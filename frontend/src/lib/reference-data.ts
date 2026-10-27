/**
 * Generated reference datasets for onboarding dropdowns.
 *
 * spec.md's global dropdown rule: "If the user has not supplied the
 * required dataset, it may be generated/populated automatically at
 * implementation time... must be meaningful, contextually correct,
 * internally consistent." These are exactly that — generated development
 * data, not a claim about any authoritative external source, and
 * replaceable later without changing how components consume them.
 */
import type { SelectOption } from "@/components/Select";

const toOptions = (values: string[]): SelectOption[] => values.map((v) => ({ value: v, label: v }));

// Country -> State -> City. A representative, searchable sample — not
// exhaustive — sufficient to demonstrate the required cascading behavior.
export const LOCATIONS: Record<string, Record<string, string[]>> = {
  India: {
    Karnataka: ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi"],
    Maharashtra: ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    Telangana: ["Hyderabad", "Warangal"],
    Delhi: ["New Delhi"],
  },
  "United States": {
    California: ["San Francisco", "Los Angeles", "San Jose"],
    "New York": ["New York City", "Buffalo"],
    Texas: ["Austin", "Dallas", "Houston"],
  },
  "United Kingdom": {
    England: ["London", "Manchester", "Birmingham"],
    Scotland: ["Edinburgh", "Glasgow"],
  },
  Germany: {
    Bavaria: ["Munich", "Nuremberg"],
    Berlin: ["Berlin"],
  },
  Canada: {
    Ontario: ["Toronto", "Ottawa"],
    "British Columbia": ["Vancouver"],
  },
};

export const COUNTRY_OPTIONS = toOptions(Object.keys(LOCATIONS));

export function stateOptionsFor(country: string | null): SelectOption[] {
  if (!country || !LOCATIONS[country]) return [];
  return toOptions(Object.keys(LOCATIONS[country]));
}

export function cityOptionsFor(country: string | null, state: string | null): SelectOption[] {
  if (!country || !state || !LOCATIONS[country]?.[state]) return [];
  return toOptions(LOCATIONS[country][state]);
}

export const GENDER_OPTIONS: SelectOption[] = [
  { value: "male", label: "Male" },
  { value: "female", label: "Female" },
  { value: "others", label: "Others" },
];

export const COLLEGE_OPTIONS = toOptions([
  "Bangalore Institute of Technology",
  "PES University",
  "RV College of Engineering",
  "MS Ramaiah Institute of Technology",
  "BMS College of Engineering",
  "Dayananda Sagar College of Engineering",
  "National Institute of Technology Karnataka",
  "Indian Institute of Technology Bombay",
  "Vellore Institute of Technology",
  "SRM Institute of Science and Technology",
  "Manipal Institute of Technology",
  "Anna University",
]);

export const DEGREE_BRANCHES: Record<string, string[]> = {
  "B.Tech": [
    "Computer Science",
    "Information Technology",
    "Electronics & Communication",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
  ],
  "B.E.": [
    "Computer Science",
    "Information Science",
    "Electronics & Communication",
    "Mechanical Engineering",
  ],
  "B.Sc": ["Computer Science", "Mathematics", "Physics", "Statistics"],
  BCA: ["Computer Applications"],
  "M.Tech": ["Computer Science", "Data Science", "VLSI Design"],
  MCA: ["Computer Applications"],
};

export const DEGREE_OPTIONS = toOptions(Object.keys(DEGREE_BRANCHES));

export function branchOptionsFor(degree: string | null): SelectOption[] {
  if (!degree || !DEGREE_BRANCHES[degree]) return [];
  return toOptions(DEGREE_BRANCHES[degree]);
}

export const ACADEMIC_YEAR_OPTIONS = toOptions([
  "2021-2025",
  "2022-2026",
  "2023-2027",
  "2024-2028",
  "2025-2029",
]);
export const CURRENT_YEAR_OPTIONS = toOptions(["1st Year", "2nd Year", "3rd Year", "Final Year"]);
export const CURRENT_SEMESTER_OPTIONS = toOptions([
  "1st Semester",
  "2nd Semester",
  "3rd Semester",
  "4th Semester",
  "5th Semester",
  "6th Semester",
  "7th Semester",
  "8th Semester",
]);
export const YEAR_OPTIONS = toOptions(Array.from({ length: 10 }, (_, i) => String(2020 + i)));
export const CGPA_SCALE_OPTIONS = toOptions(["10", "4"]);

export const SKILL_CATEGORY_OPTIONS = toOptions([
  "Programming Language",
  "Framework",
  "Database",
  "Cloud",
  "DevOps",
  "Data Structures & Algorithms",
  "System Design",
  "Soft Skill",
]);
export const PROFICIENCY_OPTIONS = toOptions(["Beginner", "Intermediate", "Advanced"]);
export const LEARNING_STATUS_OPTIONS = toOptions([
  "Just Started",
  "Learning",
  "Confident",
  "Mastered",
]);
export const COMPETITIVE_PROGRAMMING_OPTIONS = toOptions(["Beginner", "Inter-mediate", "Expert"]);

export const PROJECT_TYPE_OPTIONS = toOptions([
  "Academic",
  "Personal",
  "Freelance",
  "Open Source",
  "Hackathon",
]);
export const PROJECT_STATUS_OPTIONS = toOptions(["In Progress", "Completed", "On Hold"]);
export const TEAM_OR_INDIVIDUAL_OPTIONS = toOptions(["Individual", "Team"]);

export const CERTIFICATION_TYPE_OPTIONS = toOptions([
  "Professional",
  "Course Completion",
  "Competition",
  "Workshop",
]);

export const CAREER_INTEREST_OPTIONS = toOptions([
  "Software Development",
  "Data Science / AI",
  "Product Management",
  "Design",
  "Quality Assurance",
  "DevOps / Infrastructure",
  "Cybersecurity",
]);
export const PLACEMENT_INTEREST_OPTIONS = toOptions(["Yes", "No", "Undecided"]);
export const INTERNSHIP_INTEREST_OPTIONS = toOptions(["Yes", "No", "Undecided"]);
export const JOB_TYPE_PREFERENCE_OPTIONS = toOptions(["Full-time", "Part-time", "Internship"]);
export const REMOTE_ONSITE_HYBRID_OPTIONS = toOptions(["Remote", "On-site", "Hybrid"]);
export const PLACEMENT_STATUS_OPTIONS = toOptions([
  "Not Started",
  "Preparing",
  "Actively Applying",
  "Placed",
]);

export const PREPARATION_STATUS_OPTIONS = toOptions([
  "Not Started",
  "Just Getting Started",
  "In Progress",
  "Interview Ready",
]);
export const INTERVIEW_PREP_STATUS_OPTIONS = toOptions([
  "Not Started",
  "Learning Basics",
  "Practicing Regularly",
  "Confident",
]);
export const ASSESSMENT_PREP_STATUS_OPTIONS = toOptions([
  "Not Started",
  "Learning Basics",
  "Practicing Regularly",
  "Confident",
]);
