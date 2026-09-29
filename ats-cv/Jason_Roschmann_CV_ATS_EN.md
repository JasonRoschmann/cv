# Jason Roschmann

Junior Software Engineer · Python · FastAPI · TypeScript · Next.js · PostgreSQL · Docker Compose

Email: jason@roschmann-digital.de | Phone: +49 155 612 953 91\
LinkedIn: linkedin.com/in/jason-roschmann-1091512b2 | GitHub: github.com/JasonRoschmann | Web CV: jasonroschmann.github.io/cv\
Location: Hamburg, Germany | Looking for: Hamburg or remote; relocation to Zurich possible for the right role | Start date by arrangement

## Profile

Career changer from B2B sales, working in web development and AI automation since 2024. I develop Flowki Studio in a team, a social media studio from research to publishing, and co-founded FlowKI Club, an AI community with its own Discord bot and newsletter. For a Hamburg Shopify store, I build the translation pipeline and automated SEO checks. AI agents are my tools – I own requirements, tests and acceptance.

Key figures: <span data-pr="flowki">50</span> of my pull requests merged (Flowki Studio) · 3 store languages via my translation pipeline (DE, EN, FR) · about 66 Discord members, FlowKI Club (as of 29 Sep 2026) · 4 years of B2B sales (2019–2023)

## Core skills

- Backend & APIs: Python, FastAPI, SQLAlchemy/Alembic, PostgreSQL, Celery, Redis – APIs and background jobs in a product team
- Frontend: TypeScript, React, Next.js, Tailwind – production, approval and publishing views, community website
- Testing & CI: Git, pytest, Vitest, Playwright, GitHub Actions – every bug starts as a failing test; CI also builds and checks this CV
- AI integration: LLM APIs (Claude, Gemini, Groq), MCP, Claude Code – FAQ bot with relevance check, MCP server, model ratings checked against blind reference judgements
- Operations: Linux servers, Docker Compose, cron – rollouts with checksums, tests before and after the swap and automatic rollback
- Shopify: Liquid, Admin GraphQL API, Search Console – translation pipeline, theme rework, SEO checks
- With AI agents: Claude Code implements, I review and accept; hooks I set up block secrets in code and weakened tests, and a second model reviews
- Further tools: discord.js, React Native (personal project), Supabase, n8n, agent orchestration, Lighthouse CI, flock, SMTP/IMAP, SPF/DKIM, GSAP, PWA, Canvas/WebGL

## Experience

Since 2024: web development & AI automation in team, client and personal projects.

### Flowki Studio — internal social media studio, developer in a team (Aug 2026 – present)

Purpose: Topic research, AI-assisted content production, editorial review and publishing to social media platforms; my part: product interfaces, campaign and approval workflows, error handling, video and publishing.

- Rights before sending: Usage rights and consents were only checked at planning time, up to 14 days before the post; the studio now re-checks them right before sending and holds the post otherwise (five tests).
- Working views: Production, approval and publishing views show processing state, phase duration and required actions; checklists and open blind reviews per campaign in the daily overview.
- Team approvals: Rejection reasons flow from the interface into the approval log – posts go back for revision with a traceable reason.
- Clear error messages: When only a later status step failed after a successful production, it looked like a failure and invited a paid restart – success and follow-up errors are now reported separately.
- Video & publishing: Long videos become editable vertical clips with speaker-following framing; TikTok drafts have their own status and are clearly separated from published posts.

Tools: Python, FastAPI, Celery, SQLAlchemy/Alembic, PostgreSQL, Redis, Next.js, TypeScript

### FlowKI Club — Co-founder, community, Discord bot, website, newsletter (Apr 2026 – present)

Purpose: German-speaking AI community – about 66 members (Discord, as of 29 Sep 2026) – with articles, online calls and joint project work; I combine community work with technical product development.

- Community: Helped new members get started, organised and moderated online calls, supported members with their own AI projects.
- Discord bot: Added /ask and self-service topic roles; connected club articles as the FAQ bot's knowledge base, with a relevance check that catches unsuitable matches – covered by targeted tests.
- Website & newsletter: Newsletter with double opt-in and referral links; sign-ups and clicks on Discord invites measurable (Plausible); author, FAQ and HowTo markup for search engines.
- MCP server: Made club articles searchable and readable for AI assistants such as Claude Code; public on GitHub.

Tools: TypeScript, discord.js, Claude API, MCP, PostgreSQL, Vitest, Next.js

### duftkumpels.shop — client project, Shopify DE/EN/FR, automation & SEO (Jun 2026 – present)

- Translation: Pipeline for three languages – extract HTML texts, check their structure, import back into Shopify via CSV or GraphQL; availability checks via the Admin API with backups and read-back verification.
- SEO engineering: Automated a Search Console analysis, checked 700 URLs for indexing, added JSON-LD and checked it automatically.
- Root cause: Why English and French product pages redirected visitors to German (153 search clicks on English product pages in 90 days alone): a Shopify redirect before the theme, reproduced and documented for Shopify support.
- Theme & email: Reworked a purchased theme in Liquid, CSS and JavaScript; weekly Lighthouse checks via GitHub Actions; fixed a Klaviyo abandonment email to link to a recoverable checkout.

Tools: Shopify Liquid, Admin GraphQL API, Python, GitHub Actions, Klaviyo

### AI-assisted job application management — personal project, Python (Jul 2026 – present)

Purpose: Python pipeline that finds jobs via job board APIs (including the German Federal Employment Agency, Greenhouse, Lever), rates them, checks documents, sends applications and matches replies.

- No duplicate applications: Cross-channel ledger with reservations – at most one application per company within 14 days, whether by email or portal.
- Measure, don't assume: Checked LLM ratings against blind reference judgements; did not roll out a revised analysis without a proven improvement.
- Operations: Unusable model output stops the run and another model takes over on failure; rollouts with checksums and automatic rollback.

Evidence (German): case study reply matching <https://jasonroschmann.github.io/cv/#fs-02> · case study LLM rating <https://jasonroschmann.github.io/cv/#fs-03>

### hermes-studio — contribution to a third-party project, debugging (Sep 2026)

- Cause, not symptom: 21 failing tests, two root causes – 20× an SQLite handle that was never closed, 1× an outdated test against a security rule; rule kept, test corrected and proven with a mutation test. Passing tests: 177 → 199.
- Own contribution: Fixed silent data loss in the task store, with five new tests.

Evidence: case study on the web CV (German) <https://jasonroschmann.github.io/cv/#fs-01>

### Client websites — built in a team

- Next.js and GSAP, secured by CI with TypeScript check, ESLint, Vitest and Playwright.

Before: sales.

### B2B Direct Sales — Field sales (door-to-door) across Germany, EWE TEL and Ranger Marketing (2019 – 2023)

- Cold outreach and needs assessment with owners and managing directors, negotiation and closing on site.
- Handling rejection every day – and an eye for the problems a business really has.

## Training, certificate & languages

- Training: Web development (2024, 6 months): HTML, CSS, JavaScript, web architecture
- Certificate: Google Ads Search Certification (Skillshop), December 2025, valid until 3 Dec 2026 – verifiable: <https://www.credential.net/cd05c77a-a7ef-48e0-809e-5147135f810e>
- Languages: German (native) · English (B1, working towards B2) · Polish (spoken)
- Remote work: Distributed teamwork via GitHub (branches, pull requests), Discord and online calls
- GitHub: <span data-pr="gesamt">61</span> of my pull requests merged (as of <span data-pr="stand-en">29 Sep 2026</span>): Flowki Studio <span data-pr="flowki">50</span>, own repos <span data-pr="eigen">8</span>, client projects <span data-pr="kunden">3</span>
- Public code: web CV with build and checks <https://github.com/JasonRoschmann/cv> · MCP server for club articles <https://github.com/Jokersystems-online/flowki-knowledge-mcp>
