# Jason Roschmann

Junior Software Engineer · Python · TypeScript · AI automation

Email: jason@roschmann-digital.de | Phone: +49 155 612 953 91\
LinkedIn: linkedin.com/in/jason-roschmann-1091512b2 | GitHub: github.com/JasonRoschmann | Web CV: jasonroschmann.github.io/cv\
Location: Hamburg, Germany | Looking for: Hamburg or remote; relocation to Zurich possible for the right role | Start date by arrangement

## Profile

I build web interfaces and Python workflows for practical tasks in content production, e-commerce and community management. I focus on connecting frontend and backend, making workflow states traceable and testing failure cases. I use AI agents while taking responsibility for requirements and acceptance testing. Four years in sales taught me to understand customer needs through direct conversation.

Key figures: 50 of my pull requests merged (Flowki Studio, team project) · 21 → 0 failing tests, two root causes fixed (hermes-studio) · about 66 Discord members, FlowKI Club (as of 29 Sep 2026) · 4 years of B2B sales with daily customer contact (2019–2023)

## Projects

### Flowki Studio — internal social media studio, team project (Aug 2026 – present)

Purpose: Internal social media studio for topic research, AI-assisted content production, editorial review and handover to platforms; my contribution in the team: product interfaces, workflow integration, clip processing and publishing.

- Product interface: Further developed the production, approval and publishing views – made processing states, phase durations and required user actions visible.
- Editorial collaboration: Connected rejection reasons across the interface, API client and approval log – returns for revision now carry a traceable reason.
- Error handling: Separated successful production or licensing from subsequent status and assignment errors – removed misleading error messages and incentives for repeated, cost-incurring calls.
- Video processing: Implemented speaker-focused reframing, alternative edits and reproducible re-rendering after corrections – long videos become editable vertical clips.
- Publishing: Integrated the TikTok draft path with its own status and user notice – uploaded drafts are clearly distinguished from published posts.
- Quality assurance: Reproduced failure cases first and validated fixes with targeted tests.

Tools: Python, FastAPI, Celery, SQLAlchemy/Alembic, PostgreSQL, Redis, Next.js, TypeScript

### FlowKI Club — Co-founder, website, Discord bot, newsletter (Apr 2026 – present)

Purpose: German-speaking AI community – about 66 members (Discord, as of 29 Sep 2026) – with articles, online calls and joint project work; I combine community work with technical product development.

- Community tools: Extended the Discord bot with /ask and self-service topic roles; updated discord.js and test tooling.
- AI answer quality: Connected article content as the knowledge base of the FAQ bot and added a relevance check – tested how the bot handles irrelevant matches.
- Website & newsletter: Newsletter with double opt-in and referral links, Plausible events for sign-ups and clicks on Discord invite links; author, FAQ and HowTo markup in the article output.
- Community: Helped new members get started, organised and moderated online calls, supported members with their projects.

Tools: TypeScript, discord.js, Claude API, PostgreSQL, Vitest, Next.js

### hermes-studio — contribution to a third-party project, debugging (Sep 2026)

- Cause: 21 failing tests with two root causes – 20× an SQLite handle that was never closed and blocks cleanup on Windows, 1× an outdated test against a security rule; handle closed, rule kept, test corrected.
- Evidence: Mutation test – with the security rule weakened, the corrected test fails; passing tests: 177/198 → 199/199.
- Own contribution: Fixed silent data loss in the task store, with five new tests.

### duftkumpels.shop — client project, Shopify, API & translation automation (Jun 2026 – present)

- Automation: DE/EN/FR translation pipeline with HTML extraction, structure checks and import via CSV or GraphQL; availability checks via the Admin GraphQL API, with backups and read-back verification.
- SEO engineering: Automated a Search Console analysis, checked 700 URLs for indexing; added JSON-LD and checked it automatically.
- Theme & quality: Reworked a purchased theme in Liquid, CSS and JavaScript; weekly Lighthouse checks against the live shop via GitHub Actions.
- Email: Fixed a Klaviyo abandonment email to link to a recoverable checkout.

Tools: Shopify Liquid, Admin GraphQL API, Python, GitHub Actions, Klaviyo

### AI-assisted job application management — personal project, Python (Jul 2026 – present)

Purpose: Python pipeline for job search via job board APIs (including the German Federal Employment Agency, Greenhouse, Lever), cover letters, checks, sending and reply matching.

- Traceability: Cross-channel ledger for first applications with reservations – no duplicate application across email and portal, at most one application per company within 14 days.
- Checks before sending: Unusable model output stops the run; model cascade (Claude, Gemini, Groq) with cool-down periods.
- Rating quality: Checked LLM ratings against blind reference judgements; did not roll out a revised analysis after an incomplete measurement showed no proven improvement.
- Operations: Rollouts with checksums, tests before and after the swap and automatic rollback on caught errors.

## Experience

### AI Automation & Web Development — own projects, team and client projects (2024 – present)

- Developed and tested Python backends and Next.js frontends and ran them on Linux servers (Docker Compose, cron, deployment with rollback); customised Shopify themes; teamwork via branches, pull requests and shared test suites.
- nk247store.de (client project in a team): interactive redesign with Next.js and GSAP; CI with TypeScript check, ESLint, Vitest, build and Playwright. My redesign is not yet published.

### B2B Direct Sales — Field sales (door-to-door) across Germany, EWE TEL and Ranger Marketing (2019 – 2023)

- Cold outreach and needs assessment with owners and managing directors, negotiation and closing on site.
- Handling rejection every day – and an eye for the problems a business really has.

## Skills & way of working

- Development: Python, FastAPI · TypeScript, React, Next.js, discord.js · React Native (project experience: Shinobi)
- AI & agents: Claude Code, LLM APIs (Claude, Gemini, Groq), MCP, agent orchestration, n8n
- Data & jobs: PostgreSQL, SQLAlchemy/Alembic, Celery, Redis, Supabase
- Quality: pytest, Vitest, Playwright, GitHub Actions, Lighthouse CI
- Operations: Linux servers, Docker Compose, cron, flock, SMTP/IMAP, SPF/DKIM
- Web & commerce: Shopify Liquid, Tailwind, GSAP, PWA, Canvas/WebGL
- With AI agents: Reproduce bugs with failing tests · an agent implements the fix · a second model provides an additional review · rollout with checksums and automatic rollback on caught errors

## Training, certificate & languages

- Training: Web development (2024, 6 months): HTML, CSS, JavaScript, web architecture
- Certificate: Google Ads Search Certification (Skillshop), December 2025, valid until 3 Dec 2026 – verifiable: <https://www.credential.net/cd05c77a-a7ef-48e0-809e-5147135f810e>
- Languages: German (native) · English (B1, working towards B2) · Polish (spoken)
- Remote work: Distributed teamwork via GitHub (branches, pull requests), Discord and online calls
