---
name: MPLAD Insight
colors:
  surface: '#f9f9ff'
  surface-dim: '#cfdaf2'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e7eeff'
  surface-container-high: '#dee8ff'
  surface-container-highest: '#d8e3fb'
  on-surface: '#111c2d'
  on-surface-variant: '#444653'
  inverse-surface: '#263143'
  inverse-on-surface: '#ecf1ff'
  outline: '#757684'
  outline-variant: '#c4c5d5'
  surface-tint: '#3755c3'
  primary: '#00288e'
  on-primary: '#ffffff'
  primary-container: '#1e40af'
  on-primary-container: '#a8b8ff'
  inverse-primary: '#b8c4ff'
  secondary: '#006c4a'
  on-secondary: '#ffffff'
  secondary-container: '#82f5c1'
  on-secondary-container: '#00714e'
  tertiary: '#532a00'
  on-tertiary: '#ffffff'
  tertiary-container: '#743d00'
  on-tertiary-container: '#ffa85d'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dde1ff'
  primary-fixed-dim: '#b8c4ff'
  on-primary-fixed: '#001453'
  on-primary-fixed-variant: '#173bab'
  secondary-fixed: '#85f8c4'
  secondary-fixed-dim: '#68dba9'
  on-secondary-fixed: '#002114'
  on-secondary-fixed-variant: '#005137'
  tertiary-fixed: '#ffdcc3'
  tertiary-fixed-dim: '#ffb77d'
  on-tertiary-fixed: '#2f1500'
  on-tertiary-fixed-variant: '#6e3900'
  background: '#f9f9ff'
  on-background: '#111c2d'
  surface-variant: '#d8e3fb'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  sidebar_width: 260px
  container_max_width: 1440px
  gutter: 24px
  margin_mobile: 16px
  margin_desktop: 32px
  stack_sm: 8px
  stack_md: 16px
  stack_lg: 24px
---

## Brand & Style

The design system is engineered for high-stakes governance and public fund oversight. The visual style is **Corporate / Modern**, prioritizing information density, clarity, and institutional trust. It utilizes a refined SaaS aesthetic that balances a data-heavy environment with high readability.

The emotional response should be one of stability and precision. By using a light interface with generous white space and high-contrast typography, the design system ensures that complex financial and project data are easily digestible for government officials and auditors. Visual clutter is minimized to keep the focus on actionable insights and compliance monitoring.

## Colors

The color palette is functional and semantic, designed to communicate status at a glance without overwhelming the user.

- **Primary (#1E40AF):** A deep indigo used for primary actions, active navigation states, and branding elements. It conveys authority and reliability.
- **Success/Low Risk (#059669):** Used for positive trends, completed projects, and "Healthy" fund status.
- **Warning/Medium Risk (#D97706):** Used for pending approvals, minor delays, or moderate fund utilization gaps.
- **Critical/High Risk (#DC2626):** Reserved for immediate attention items, such as fund lapses, stalled projects, or compliance violations.
- **Neutral/Background:** The app uses a layered grayscale approach. The main canvas is **#F1F5F9**, while primary surfaces (cards, tables) are pure **#FFFFFF** to create a clear "object-on-ground" relationship. Text utilizes Deep Slate (**#1E293B**) for maximum legibility against light backgrounds.

## Typography

This design system utilizes **Inter** exclusively to maintain a systematic and utilitarian feel. The type hierarchy is strictly defined to handle multi-level data displays.

- **Headlines:** Use tighter letter spacing and heavier weights to anchor sections and page headers.
- **Body Text:** Standardized at 14px for data tables and 16px for prose to maximize information density while remaining accessible.
- **Labels:** Small, all-caps labels are used for table headers and secondary metadata to differentiate them from interactive data points.
- **Numerical Data:** For financial figures, ensure the use of tabular num alignment (tnum) to allow for easy vertical scanning of columns in data tables.

## Layout & Spacing

The layout follows a **Fixed-Fluid Hybrid** model. 
- **Sidebar:** A persistent 260px left navigation bar anchors the application.
- **Main Canvas:** A fluid area that expands to a maximum of 1440px. On ultra-wide monitors, the content centers with margins.
- **Grid:** A 12-column grid is used within the main canvas for dashboard widgets.
- **Breakpoints:**
  - **Desktop (1280px+):** 12 columns, 32px margins.
  - **Tablet (768px - 1279px):** 6 columns, 24px margins. Sidebar collapses to an icon-only rail or hides behind a hamburger menu.
  - **Mobile (< 767px):** 4 columns, 16px margins. Cards stack vertically.

The spacing rhythm is based on an **8px linear scale**, ensuring consistent vertical rhythm between form fields, text blocks, and components.

## Elevation & Depth

To maintain a clean, professional "flat" look while ensuring hierarchy, this design system uses **Tonal Layers** supplemented by very soft, functional shadows.

- **Level 0 (Background):** #F1F5F9. Used for the base canvas.
- **Level 1 (Cards/Surfaces):** Pure white (#FFFFFF). These elements feature a 1px border in #E2E8F0 and a very subtle drop shadow: `0px 1px 3px rgba(0, 0, 0, 0.1)`.
- **Level 2 (Popovers/Modals):** High-elevation surfaces use a more pronounced shadow: `0px 10px 15px -3px rgba(0, 0, 0, 0.1)` to pull the user's attention forward.
- **Interactive States:** Buttons and interactive cards do not lift on hover; instead, they use a subtle background color shift (e.g., Primary Blue moves to a slightly darker shade) to indicate state.

## Shapes

The shape language is structured and "Soft-Industrial." 

- **Cards & Primary Containers:** Use a 8px (`rounded-lg`) corner radius to soften the enterprise environment without appearing too casual.
- **Buttons & Input Fields:** Use a matching 8px radius to maintain consistency.
- **Status Badges/Chips:** Utilize a fully rounded (pill-shaped) radius to distinguish them from interactive buttons.
- **Data Visualizations:** Bar charts should use slight rounding (2-4px) on the top corners of bars to align with the overall UI aesthetic.

## Components

### Buttons & Inputs
- **Primary Action:** Solid #1E40AF background with white text. 8px radius.
- **Secondary Action:** Ghost style with #1E40AF border and text.
- **Inputs:** 1px #CBD5E1 border, white background. On focus, the border changes to #1E40AF with a subtle 2px outer glow.

### KPI Cards
- Large "Display" font size for the primary metric.
- A small trend indicator (e.g., "↑ 12%") positioned in the bottom right, color-coded by the semantic palette (Red/Green).
- A subtle sparkline (line chart) may be embedded at the bottom of the card.

### Data Tables
- **Header:** Light gray background (#F8FAFC) with uppercase `label-md` typography.
- **Rows:** White background with 1px bottom border (#F1F5F9). High-risk rows can have a very faint 2px left-border highlight in Red (#DC2626).
- **Severity Badges:** High-contrast text on low-opacity backgrounds (e.g., Red text on 10% opacity red background) for maximum readability without visual noise.

### Navigation
- **Sidebar:** Dark theme variant for the sidebar is permitted (using #1E293B) to provide strong visual separation from the content area, or a clean white sidebar with a 1px right border.
- **Active State:** A solid left-edge accent bar (4px width) in Primary Blue to indicate the current section.

### Charts
- Use a palette derived from the Primary and Status colors. Avoid high-saturation "rainbow" charts; prefer monochromatic blue scales for multi-category bar charts, reserving Red/Amber/Green strictly for risk-related data.