# GTM Labs Component Catalog

Complete index of all components available via the GTM Labs MCP Server.

## 📦 How to Access

Use any of these commands in Windsurf:
```
"Use GTM Labs MCP to get [component-name]"
"Use GTM Labs MCP to list components in [category]"
"Use GTM Labs MCP to show specs for [component-name]"
```

---

## 🎯 Sections

Full-page sections with content and layouts.

### `how-we-help-section`
**Path:** `components/ui/how-we-help-section.tsx`  
**Description:** Alternating two-column layout with animations for each row  
**Dependencies:** 
- `TwoColumnFeature` (cosmic)
- `MiniFeatureCard` (cosmic)
- `MultiplierAnimation`, `BalanceScaleAnimation`, `FogLiftAnimation`, `FlywheelAnimation`
- `lucide-react` icons

**Features:**
- 4 rows of alternating content
- Custom animations per row
- Gradient text headline
- Mini feature cards with icons

---

### `how-it-works-section`
**Path:** `components/ui/how-it-works-section.tsx`  
**Description:** Process/timeline section

---

### `content-library-cards`
**Path:** `components/ui/content-library-cards.tsx`  
**Description:** Content library display cards

---

### `alternating-section`
**Path:** `components/ui/alternating-section.tsx`  
**Description:** Generic alternating content section layout

---

## 🎨 Animations

Animation components and utilities.

### `how-we-help-animations`
**Path:** `components/ui/how-we-help-animations.tsx`  
**Description:** Custom animations for how-we-help section  
**Animations:**
- `MultiplierAnimation`
- `BalanceScaleAnimation`
- `FogLiftAnimation`
- `FlywheelAnimation`

---

## 🧩 UI Components

Reusable UI building blocks.

### Buttons
- `button` - Base button component
- `hero-button` - Specialized hero section button
- `shimmer-button` - Button with shimmer effect (magicui)
- `ripple-button` - Button with ripple effect (magicui)

### Cards
- `card` - Base card component
- `3d-card` - 3D effect card
- `display-cards` - Display card variants
- `analytics-cards` - Analytics-focused cards

### Inputs & Forms
- `input` - Base input component
- `label` - Form label component
- `animated-glowing-search-bar` - Search bar with glow effect

### Other UI
- `banner` - Banner component
- `inline-tooltip` - Tooltip component
- `progressive-blur` - Progressive blur effect

---

## ✨ Cosmic Design System

Custom design system components.

### Layout Components
- `TwoColumnFeature` - Two-column feature layout
- `MiniFeatureCard` - Small feature card with icon

### Visual Components
- `cosmic-background` - Animated cosmic background
- `cosmic-button` - Styled button
- `cosmic-glow-card` - Card with glow effect
- `cosmic-header` - Header component
- `cosmic-pill` - Pill-shaped element
- `glass-card` - Glass morphism card

### Integration & Display
- `cosmic-integration-card` - Integration card
- `cosmic-marquee` - Scrolling marquee
- `integration-grid` - Grid of integrations

### Interactive
- `feature-tabs` - Tabbed feature display
- `browser-frame` - Browser window frame

---

## 🪄 MagicUI Components

Magic UI library components.

### Effects
- `animated-beam` - Animated connecting beams
- `blur-fade` - Blur fade transition
- `border-beam` - Animated border effect
- `shine-border` - Shining border effect
- `shimmer-border` - Shimmering border

### Interactive
- `dock` - macOS-style dock
- `magic-card` - Magic effect card

---

## 🧪 Experiments

Experimental and testing components.

### Bento Grids
- `BentoGrid` - Base bento grid
- `BentoSection` - Bento section layout
- `BentoSectionOptionA/B/C` - Variants

---

## 🎭 Other Components

### Text Effects
- `TextFlip` - Text flip animation
- `container-text-flip` - Container with text flip

### Interactive
- `interactive-demo` - Interactive demonstration component
- `interactive-pricing` - Interactive pricing component
- `interactive-pricing-section` - Full pricing section

### Specialized
- `demo` - Demo component
- `discussion` - Discussion/comment component
- `customization-graph` - Customization visualization
- `problem-parallax-cards` - Parallax card effect
- `ruixen-featured-image-section` - Featured image section

---

## ⚙️ Configuration Files

Access design tokens, configs, and utilities.

### Design Tokens
**Path:** `lib/design-tokens.ts`  
**Contains:**
- Color system (primary, sidebar, blue, status, gray, semantic)
- Typography (fonts, sizes, weights)
- Spacing values
- Border radius values
- Shadows (elevation system)
- Animation (duration, easing)
- Component-specific tokens

**Access via:**
```
"Use GTM Labs MCP to get design-tokens"
"Show me the color palette from design tokens"
```

### Tailwind Config
**Path:** `tailwind.config.ts`  
**Contains:**
- Extended color palette
- Custom animations (skew-scroll, shiny-text, bloop, pulse-slow, spin-slow)
- Font configuration (Geist Sans, Geist Mono)
- Custom spacing and sizing
- Shadow system
- Border radius variants

**Access via:**
```
"Use GTM Labs MCP to get tailwind config"
```

### Utilities
**Path:** `lib/utils.ts`  
**Contains:** Helper functions and utilities

**Path:** `lib/brand.ts`  
**Contains:** Brand-specific constants

---

## 📐 Layouts

Page layouts and templates.

### Two-Column Alternating Layout
Used in `how-we-help-section` - alternating text and visual content.

**Pattern:**
```tsx
<TwoColumnFeature
  eyebrow="Label"
  title="Section Title"
  description="Description text"
  imageFrame="plain"
  image={<AnimationComponent />}
>
  <MiniFeatureCard ... />
  <MiniFeatureCard ... />
  <MiniFeatureCard ... />
</TwoColumnFeature>
```

---

## 🎨 Design Specs

### Color Palette

**Primary Colors:**
- Primary: `#8b5cf6` (purple)
- Sidebar: `#3f0e40` (aubergine)
- Blue: `#1264a3` (ThreadFolio blue)

**Semantic Colors:**
- Success: `#22c55e` (green)
- Warning: `#f59e0b` (yellow/orange)
- Danger: `#ef4444` (red)

**Grays:**
- From `#fcfcfd` (25) to `#0a0a0a` (950)

### Typography

**Font Family:**
- Sans: Geist Sans, system-ui, sans-serif
- Mono: Geist Mono, monospace

**Font Sizes:**
- xs: 12px → 9xl: 128px
- Base: 15px with 28px line-height

### Animations

**Keyframes:**
- `skew-scroll` - 3D scrolling effect
- `shiny-text` - Shimmering text
- `accordion-down/up` - Accordion transitions
- `fade-in` - Fade in effect
- `slide-in-from-left/bottom` - Slide transitions
- `bloop` - Scale bounce
- `pulse-slow` - Slow pulsing
- `spin-slow` - Slow rotation

**Durations:**
- Fast: 100ms
- Default: 200ms
- Slow: 300ms

### Spacing

Uses standard Tailwind spacing with custom values:
- Compact: 0.25rem → 1.5rem
- Standard: 1rem → 6rem

---

## 🚀 Quick Start Examples

### Get a Complete Section
```
"Use GTM Labs MCP to get how-we-help-section with all dependencies"
```

### Check Component Styles
```
"Use GTM Labs MCP to show me what colors hero-section uses"
"What animations does the cosmic-card use?"
"Show me the border styles in the glass-card"
```

### Build a Page
```
"Use GTM Labs MCP to create a landing page with:
- hero-section
- how-we-help-section  
- content-library-cards
- cosmic-button components"
```

### Version Control
```
"Get hero-section from version v1.0.0"
"Show changelog for how-we-help-section"
```

---

## 📊 Component Statistics

**Total Components:** 37+ in `/components/ui/`  
**Design Tokens:** 256 lines  
**Tailwind Config:** 270 lines  
**Categories:** 7 (sections, navigation, animations, ui, cosmic, magicui, experiments)

---

## 🔍 Search Tips

Use natural language to find components:

```
"Find components with animation effects"
"Search for button components"
"Show me all card components"
"List components using framer-motion"
"Find components with gradient effects"
```

---

## 📝 Notes

- All components use TypeScript/TSX
- Styling via Tailwind CSS
- Animations via Framer Motion
- Icons via Lucide React
- Design system: Custom "Cosmic" + MagicUI
- All components are "use client" (React Client Components)

---

**Last Updated:** Project scan completed  
**MCP Version:** 1.0.0  
**Total Accessible Resources:** 50+
