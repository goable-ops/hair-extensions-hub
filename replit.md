# Hair Extensions Hub

## Overview
Hair Extensions Hub is a premium Flask-based multi-page site for a mobile weft extension specialist (Donna) servicing the City of Moreton Bay. The site sells a $27 digital guide via Stan Store and accepts weft service booking requests. Full premium dark theme with champagne gold brand identity.

## User Preferences
- Preferred communication style: Simple, everyday language
- Weft services only (no tape, clip-in, or machine weft)
- Digital product sales via Stan Store ($27)
- Mobile weft specialist — she comes to the client
- No Instagram; TikTok (@hair.extensions.hub) + Facebook only
- City of Moreton Bay focus

## Brand Identity
- **Colours**: Dark warm ink `#1A1208` (background), champagne gold `#C9A96E` (accent), cream `#FAF6EF` (text)
- **Typography**: Cormorant Garamond (serif display) + Jost (body sans)
- **Tone**: Premium, honest, warm — no jargon

## System Architecture

### Application Framework
**Technology**: Flask (Python web framework)
**Routes**:
- `/` — Homepage
- `/wefts` — Services & pricing + booking form
- `/digital` — Digital guides & products
- `/weft-booking` (POST) — Saves booking submission + sends email
- `/digital-notify` (POST) — Saves waitlist signup

### External Services
- **Stan Store**: https://stan.store/hairextensionshub — digital guide ($27) checkout
- **Resend**: Email notifications for weft bookings (resend==1.0.0 installed)
- **Facebook**: https://www.facebook.com/share/1DFyqa13Nu/
- **TikTok**: https://www.tiktok.com/@hair.extensions.hub
- **Google reviews**: https://share.google/j6ou7afkEtmcL3jNB

## Project Structure
```
├── app.py                        # Flask routes for all pages and form submissions
├── templates/
│   ├── index.html                # Homepage — split hero, marquee, image strip, how-it-works,
│   │                             #   img-break, grams calculator (6-step JS), 5★ reviews,
│   │                             #   before/after grid + video, two-path CTA, final CTA
│   ├── wefts.html                # Services page — pricing tabs (4 types), booking steps,
│   │                             #   Facebook Marketplace callout bar, booking form
│   ├── digital.html              # Digital products — $27 featured guide, coming-soon cards,
│   │                             #   waitlist notify form, "why digital" section
│   ├── thankyou.html             # Thank you page (personalised plan)
│   └── booking_thankyou.html     # Thank you page (weft booking)
├── submissions/                  # JSON files from all form submissions
└── static/
    ├── images/
    │   ├── donna.png             # Donna's photo (used in hero + before/after grid)
    │   ├── before-after-1.jpg    # Before/after result 1
    │   └── before-after-2.jpg    # Before/after result 2
    └── videos/
        ├── transformation1.mp4
        └── transformation2.mp4
```

## Pages

### Home Page (/)
- Split-screen hero (before-after photo left, Donna photo right)
- Gold marquee ticker
- 3-panel image strip
- 3-step process section
- Full-width before/after photo break
- 6-step grams calculator (JavaScript, fully functional, no backend needed)
- 5.0-star reviews section with 3 real Google review quotes
- Before/after grid (2 photos + 1 video + 2 social placeholders + 1 Donna photo)
- Two-path CTA cards ($27 guide vs in-person service)
- Final CTA with Donna photo background

### Wefts Page (/wefts)
- Page hero with pill tags
- Facebook Marketplace callout bar (→ Book Now)
- What's included strip
- Three weft type cards (Premium Flat, Mini/Genius Premium, Mini/Genius Luxury)
- Tabbed pricing tables (4 tabs: Flat, Mini Premium, Mini Luxury, Maintenance)
- 3-step booking process explainer
- Booking request form (POST → /weft-booking)
- Aftercare grid (6 cards)

### Digital Page (/digital)
- Dark hero with distinction panel (digital vs in-person)
- Gold marquee ticker
- Featured product: $27 guide → Stan Store
- 3 coming-soon product cards (Masterclass, Calculator, Colour Guide)
- Notify waitlist form (POST → /digital-notify)
- "Why digital" section
- CTA footer

## Form Fields

### Weft Booking (/weft-booking POST)
- name, mobile, email, suburb (NOT location), service, weft_type (NOT weftType), length, grams, notes

### Digital Notify (/digital-notify POST)
- notify_name, notify_email

## Product Information

### Main Product
- **Product**: The Ultimate Hair Extensions Guide
- **Price**: $27 AUD (one-time, instant download)
- **Via**: Stan Store (https://stan.store/hairextensionshub)

### Weft Services (mobile, City of Moreton Bay only)
- Premium Flat Weft (Russian Premium): $350–$1,220 depending on length/grams
- Mini / Genius Weft (Premium): $420–$1,650
- Mini / Genius Weft (Luxury): $540–$2,000+
- Maintenance / move-up: $120–$330 depending on rows
- Fix-ups & styling: $150/hour

## Deployment
- Nix channel must be `stable-24_05` (not `stable-25_05`)
- Simple Flask app, no database, submissions saved as JSON files to `submissions/`
