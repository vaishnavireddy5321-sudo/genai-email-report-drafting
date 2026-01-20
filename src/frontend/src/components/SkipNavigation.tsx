/**
 * SkipNavigation component for keyboard accessibility
 * Provides a skip link for keyboard users to bypass navigation and go directly to main content
 * Implements WCAG 2.1 Level AA guideline 2.4.1 (Bypass Blocks)
 */

export default function SkipNavigation() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-primary-600 focus:text-white focus:px-4 focus:py-2 focus:rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
    >
      Skip to main content
    </a>
  );
}
