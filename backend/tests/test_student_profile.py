from backend.tests.conftest import complete_registration

STUDENT_MOBILE = "9812340001"


def _register_student(client, mobile: str = STUDENT_MOBILE) -> str:
    res = client.post("/api/auth/send-otp", json={"mobile_number": mobile, "purpose": "register"})
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp", json={"mobile_number": mobile, "code": otp, "purpose": "register"}
    )
    return complete_registration(client, mobile, res.json()["token"])


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_basic_info_requires_authentication(client):
    res = client.get("/api/students/me/basic-info")
    assert res.status_code == 401


def test_basic_info_roundtrip(client):
    # Student Create Account UPDATE SDD: a real student account only ever
    # exists once Create Account has run, which requires Basic Information
    # to already be present — so there is no "account with no Basic
    # Information yet" state to observe here; `complete_registration`'s
    # own placeholder values are what a freshly created account starts
    # with, and this test's actual subject is that a PUT genuinely
    # updates them.
    token = _register_student(client)
    headers = _auth_headers(token)

    res = client.get("/api/students/me/basic-info", headers=headers)
    assert res.status_code == 200
    assert res.json()["full_name"] == "Test Student"

    payload = {
        "full_name": "Asha Rao",
        "date_of_birth": "2003-04-12",
        "gender": "female",
        "email": "asha.rao@example.com",
        "country": "India",
        "state": "Karnataka",
        "city": "Bengaluru",
    }
    res = client.put("/api/students/me/basic-info", json=payload, headers=headers)
    assert res.status_code == 200
    assert res.json()["full_name"] == "Asha Rao"

    res = client.get("/api/students/me/basic-info", headers=headers)
    assert res.json()["email"] == "asha.rao@example.com"


def test_basic_info_rejects_invalid_email_and_gender(client):
    token = _register_student(client, "9812340002")
    headers = _auth_headers(token)

    bad_payload = {
        "full_name": "Test",
        "date_of_birth": "2003-04-12",
        "gender": "unknown",
        "email": "not-an-email",
        "country": "India",
        "state": "Karnataka",
        "city": "Bengaluru",
    }
    res = client.put("/api/students/me/basic-info", json=bad_payload, headers=headers)
    assert res.status_code == 422


def test_academic_info_roundtrip(client):
    token = _register_student(client)
    headers = _auth_headers(token)
    payload = {
        "college": "Test Institute of Technology",
        "degree": "B.Tech",
        "branch": "Computer Science",
        "academic_year": "2023-2027",
        "current_year": "2nd Year",
        "current_semester": "4th Semester",
        "admission_year": "2023",
        "expected_graduation_year": "2027",
        "current_cgpa": 8.4,
        "cgpa_scale": "10",
    }
    res = client.put("/api/students/me/academic-info", json=payload, headers=headers)
    assert res.status_code == 200
    assert res.json()["college"] == "Test Institute of Technology"


def test_multiple_skills_with_evidence(client):
    token = _register_student(client)
    headers = _auth_headers(token)

    res = client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Python",
            "skill_category": "Programming Language",
            "proficiency": "Intermediate",
            "learning_status": "Learning",
        },
        headers=headers,
    )
    assert res.status_code == 200
    skill_id = res.json()["id"]

    client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "SQL",
            "skill_category": "Database",
            "proficiency": "Beginner",
            "learning_status": "Learning",
        },
        headers=headers,
    )

    res = client.post(
        f"/api/students/me/skills/{skill_id}/evidence",
        json={"description": "Built a Flask API", "link": "https://github.com/example/repo"},
        headers=headers,
    )
    assert res.status_code == 200

    res = client.get("/api/students/me/skills", headers=headers)
    skills = res.json()
    assert len(skills) == 2
    python_skill = next(s for s in skills if s["skill_name"] == "Python")
    assert python_skill["evidence"][0]["description"] == "Built a Flask API"

    res = client.delete(f"/api/students/me/skills/{skill_id}", headers=headers)
    assert res.status_code == 204
    res = client.get("/api/students/me/skills", headers=headers)
    assert len(res.json()) == 1


def test_projects_and_certifications_support_multiple_entries(client):
    token = _register_student(client)
    headers = _auth_headers(token)

    for name in ("Portfolio Site", "Chat App"):
        res = client.post(
            "/api/students/me/projects",
            json={"project_name": name, "technologies_used": ["React", "Node.js"]},
            headers=headers,
        )
        assert res.status_code == 200

    res = client.get("/api/students/me/projects", headers=headers)
    assert len(res.json()) == 2
    assert res.json()[0]["technologies_used"] == ["React", "Node.js"]

    res = client.post(
        "/api/students/me/certifications",
        json={"certification_name": "AWS Cloud Practitioner", "skills_covered": ["AWS"]},
        headers=headers,
    )
    assert res.status_code == 200
    cert_id = res.json()["id"]

    res = client.delete(f"/api/students/me/certifications/{cert_id}", headers=headers)
    assert res.status_code == 204


def test_certificate_file_upload(client):
    import io

    token = _register_student(client)
    headers = _auth_headers(token)

    cert = client.post(
        "/api/students/me/certifications",
        json={"certification_name": "AWS Cloud Practitioner", "skills_covered": ["AWS"]},
        headers=headers,
    ).json()
    assert cert["certificate_file_path"] is None

    res = client.post(
        f"/api/students/me/certifications/{cert['id']}/file",
        headers=headers,
        files={"file": ("cert.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    assert res.status_code == 200
    assert res.json()["certificate_file_path"] is not None

    certs = client.get("/api/students/me/certifications", headers=headers).json()
    assert certs[0]["certificate_file_path"] is not None


def test_certificate_file_upload_requires_ownership(client):
    import io

    token_a = _register_student(client, "9812340002")
    token_b = _register_student(client, "9812340003")
    headers_a = _auth_headers(token_a)
    headers_b = _auth_headers(token_b)

    cert = client.post(
        "/api/students/me/certifications",
        json={"certification_name": "AWS Cloud Practitioner"},
        headers=headers_a,
    ).json()

    res = client.post(
        f"/api/students/me/certifications/{cert['id']}/file",
        headers=headers_b,
        files={"file": ("cert.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    assert res.status_code == 404


def test_onboarding_status_reflects_saved_sections(client):
    # Student Create Account UPDATE SDD: Create Account requires Basic
    # Information to already be set, so a freshly created account starts
    # with `basic_info_complete: True`, not every section unset.
    token = _register_student(client)
    headers = _auth_headers(token)

    res = client.get("/api/students/me/onboarding-status", headers=headers)
    assert res.json() == {
        "basic_info_complete": True,
        "academic_info_complete": False,
        "has_skills": False,
        "has_coding_experience": False,
        "has_projects": False,
        "has_certifications": False,
    }

    client.put(
        "/api/students/me/basic-info",
        json={
            "full_name": "Test Student",
            "date_of_birth": "2003-01-01",
            "gender": "others",
            "email": "test@example.com",
            "country": "India",
            "state": "Karnataka",
            "city": "Mysuru",
        },
        headers=headers,
    )
    res = client.get("/api/students/me/onboarding-status", headers=headers)
    assert res.json()["basic_info_complete"] is True


def test_student_cannot_access_another_students_data(client):
    token_a = _register_student(client, "9812340098")
    token_b = _register_student(client, "9812340099")

    client.post(
        "/api/students/me/skills",
        json={
            "skill_name": "Java",
            "skill_category": "Programming Language",
            "proficiency": "Advanced",
            "learning_status": "Confident",
        },
        headers=_auth_headers(token_a),
    )

    # Student B's own skill list must not include Student A's skill.
    res = client.get("/api/students/me/skills", headers=_auth_headers(token_b))
    assert res.json() == []


def test_recruiter_cannot_access_student_endpoints(client):
    res = client.post(
        "/api/auth/send-otp", json={"mobile_number": "9999999999", "purpose": "login"}
    )
    otp = res.json()["dev_otp"]
    res = client.post(
        "/api/auth/verify-otp",
        json={"mobile_number": "9999999999", "code": otp, "purpose": "login"},
    )
    recruiter_token = res.json()["token"]

    res = client.get("/api/students/me/basic-info", headers=_auth_headers(recruiter_token))
    assert res.status_code == 403
