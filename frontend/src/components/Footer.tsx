import * as React from "react";

export interface FooterLink {
  label: string;
  onClick?: () => void;
  to?: string;
}

/** Global footer — spec.md §14/§17-23. Content (which links, copyright
 * text) is supplied by each portal; the structure/styling is shared and
 * must never be redesigned per page. */
export function Footer({ links, copyright }: { links: FooterLink[]; copyright: React.ReactNode }) {
  return (
    <footer className="lm-footer">
      <div className="lm-footer__links">
        {links.map((link) =>
          link.to ? (
            <a key={link.label} href={link.to}>
              {link.label}
            </a>
          ) : (
            <button
              key={link.label}
              type="button"
              className="lm-footer__link"
              onClick={link.onClick}
            >
              {link.label}
            </button>
          ),
        )}
      </div>
      <div>{copyright}</div>
    </footer>
  );
}
