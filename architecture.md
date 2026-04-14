# Project Document: AI-Powered CBEC KOL Marketing Content Platform

**Version:** 1.1 (English)
**Date:** May 20, 2025
**Author:** [Your Name/Team Name]

## 1. Introduction

### 1.1. Project Overview
This project aims to develop an AI-powered, multi-agent platform designed to streamline and enhance the marketing content creation process for Chinese Brands Going Global (CBEC) when collaborating with international Key Opinion Leaders (KOLs). The system will assist in generating localized content, managing brand consistency, and improving the efficiency of providing marketing materials to KOLs.

### 1.2. Core Value Proposition
* **Efficiency:** Drastically reduce the time and effort required to create and adapt marketing materials for multiple international KOLs and platforms.
* **Localization:** Generate content that is culturally relevant and resonates with target overseas audiences, moving beyond simple translation.
* **Quality & Consistency:** Improve the quality of KOL briefs and marketing assets, ensuring brand messaging is consistent while allowing for KOL creativity.
* **Empowerment & Collaboration:** Provide brands and marketing agencies (e.g., your sister's business) with a powerful tool to manage complex cross-border content strategies and execution.

### 1.3. Target Users
* **Primary Users:** Marketing agencies and consultants specializing in helping Chinese brands expand internationally via KOL marketing (e.g., your sister's business).
* **Secondary Users:** Marketing teams within Chinese brands that are directly managing their international KOL campaigns.

## 2. System Architecture Overview

The system will be built around a **Multi-Agent Architecture**, where specialized AI agents collaborate to perform tasks throughout the content lifecycle.

### Key Agents & Roles:
1.  **Orchestrator Agent:** Manages the overall workflow, data flow, and communication between other agents.
2.  **Planner Agent (Localization Strategist):** Analyzes brand/product info, target market, and KOL profiles to generate localized marketing angles, content themes, and platform-specific strategies. Utilizes a **Localization Knowledge Base**.
3.  **Writer Agent (Multi-lingual/Style Copywriter):** Generates draft copy (social media posts, video script outlines, ad copy) in the target language, adapting to different KOL styles and platform requirements.
4.  **Image Agent (Visual Concept Advisor & Processor):** Suggests visual concepts, styles, and specific image/video requirements. (Future: AI image generation).
5.  **Refiner Agent (Text Micro-Tuner & Version Generator):** Allows users to perform guided, non-disruptive fine-tuning of AI-generated text (e.g., "make more concise," "change tone to informal") and generate multiple optimized versions. **This is a key differentiating feature.**
6.  **Branding Agent (Brand Asset Customizer):** Adds brand elements like logos, watermarks, and potentially applies brand color palettes/fonts to visual concepts or assets.
7.  **Text Critic Agent:** Reviews generated/refined text against brand guidelines, localization best practices, and quality standards.
8.  **Image Critic Agent:** Reviews visual concepts/branded images for alignment with brand aesthetics and campaign goals.
9.  **Decision Agents (Text/Image):** Based on Critic Agent feedback (and potentially user input), decides if content passes to the next stage or needs revision.
10. **Distributor Agent (Future Enhancement):** Facilitates content packaging for different platforms and, eventually, direct publishing.

## 3. Technology Stack Recommendations

* **Backend:** Python (FastAPI preferred for AI/ML integration, ease of use, and large ecosystem).
* **Frontend:** React Vite for a modern, interactive UI.
* **Database:**
    * PostgreSQL (Supabase): For structured data like user accounts, brand profiles, project settings. for storing less structured content drafts, agent outputs, or the Localization Knowledge Base.
* **AI/LLM Integration:**
    * Primary LLMs: Gemini family. These have strong English capabilities crucial for Western markets.
    * Secondary/Supplementary LLMs: Consider leading Chinese LLMs (e.g., Ernie Bot, QWen via OpenRouter) if significant Chinese language processing or culturally specific Chinese brand understanding is needed as input to the localization process.
    * Multi-agent system: Agents Development Kit (ADK) by Google as the framework to implement multi-agents.
    * Strategy: Use more powerful/costly models for complex tasks (Planner, Refiner) and more economical models for simpler, high-volume tasks.
* **Image Processing:**
    * Backend: Pillow (Python library) for basic logo/watermark application.
    * Frontend/Backend: For more advanced image manipulation or suggestions.
    * Future AI Image Generation: APIs like Gemini image creation.
* **Task Queues & Background Jobs:** Celery with Redis or RabbitMQ for handling asynchronous tasks like LLM calls, batch processing, and report generation.
* **Localization Knowledge Base:** Could be a vector database (e.g., Qdrant, Chroma) populated with curated information about target markets, cultural nuances, platform best practices, and successful CBEC campaigns. Use Retrieval Augmented Generation (RAG) with the Planner Agent.
* **Deployment:** Local Development for now.
* **Version Control:** Git (GitHub, GitLab, Bitbucket).

## 4. Core Agent Implementation Details (Conceptual)

*(For each agent, define its purpose, inputs, core logic using LLMs – including example prompt strategies or RAG approach – and outputs.)*

**Example: Planner Agent (Localization Strategist)**
* **Purpose:** Translate Chinese brand essence into effective marketing strategies for specific overseas markets and KOL types.
* **Inputs:** Brand guidelines, product SKUs/details (can be in Chinese), target market selection (e.g., "US Gen Z females on TikTok"), KOL archetype (e.g., "quirky unboxing expert").
* **Core Logic (LLM + RAG):**
    1.  **Deconstruct Input:** LLM analyzes brand info & product details.
    2.  **Retrieve Relevant Knowledge:** Query the Localization Knowledge Base (vector DB) for insights related to the target market, platform (TikTok), KOL archetype (unboxing), and product category. Retrieved info includes cultural sensitivities, trending content formats, effective CTAs, common slang/references.
    3.  **Synthesize Strategy (Example Prompt Strategy):**
        ```
        Prompt to LLM:
        "You are an expert Cross-Border E-commerce Marketing Strategist.
        Brand: [Brand Name], Core Values: [Values], Product: [Product Name], Key Features (Chinese): [Features_CN], Target Price Point: [Price].
        Target Audience: US Gen Z females on TikTok. KOL Archetype: Quirky unboxing expert.
        Retrieved Cultural Insights for US Gen Z: [Insight 1, Insight 2...].
        Retrieved TikTok Trends for Unboxing: [Trend A, Trend B...].

        Based on all this, propose 3 distinct localized content angles for this KOL to showcase the product.
        For each angle, suggest:
        1. Core Message (localize from Chinese features, highlight benefits for US Gen Z).
        2. Content Format/Style (e.g., fast-paced edit, trending sound, specific TikTok challenge).
        3. Key Visual Elements to emphasize.
        4. Call to Action appropriate for the platform and audience.
        Ensure the angles are authentic and avoid direct translation pitfalls."
        ```
* **Outputs:** Structured strategy document: suggested content angles, core messages (in English), recommended content formats, visual cues, CTAs.

**Example: Refiner Agent (Text Micro-Tuner)**
* **Purpose:** Enable quick, intuitive, non-disruptive modifications to AI-generated text.
* **Inputs:** AI-generated text snippet, user selection/highlighting of text, user choice of refinement action (e.g., "Make more concise," "Change tone to 'excited'," "Suggest 3 alternative phrases for [selected part]").
* **Core Logic (LLM):**
    1.  User selects text and an action (e.g., "Make this sentence more punchy").
    2.  **Example Prompt Strategy:**
        ```
        Prompt to LLM:
        "Original sentence: '[Selected Sentence]'
        User request: 'Make this sentence more punchy.'
        Rewrite the sentence to be more punchy and engaging for a TikTok caption, while retaining the core meaning. Provide 1-2 options."
        ```
    3.  Or, for "Suggest alternatives":
        ```
        Prompt to LLM:
        "Context: '[Surrounding paragraph or full text]'
        Selected phrase for alternatives: '[Selected Phrase]'
        Suggest 3 alternative ways to phrase '[Selected Phrase]' that fit the overall context and are suitable for an Instagram post by a beauty influencer."
        ```
* **Outputs:** Modified text snippet or list of alternative phrases.

*(Continue this detailed breakdown for Writer, Image, Branding, Text Critic, Image Critic, and Decision Agents)*

## 5. Key Feature Implementation Walkthroughs (High-Level)

*(Detail how a user would interact with the system for common tasks, and which agents are involved.)*

**A. New CBEC Campaign Setup:**
1.  User (Agency/Brand) creates a new project.
2.  Inputs: Brand assets (guidelines, logo), product details, target markets, campaign goals, initial KOL profile ideas.
3.  Data stored in DB, linked to the project.
4.  **Orchestrator** triggers **Planner Agent**.

**B. Generating a KOL Content Package:**
1.  Planner Agent outputs localized strategy. User reviews/approves.
2.  Orchestrator sends strategy to **Writer Agent** & **Image Agent**.
3.  Writer outputs draft copy variations. Image Agent outputs visual concept guides.
4.  Orchestrator sends copy to **Refiner Agent**. User interacts with Refiner to fine-tune text.
5.  Refined text to **Text Critic Agent** -> **Text Decision Agent**. Loop if revisions needed.
6.  Visual concepts (and approved text for context) to **Branding Agent**. Branding Agent outputs branded visual mockups/guides.
7.  Branded visuals to **Image Critic Agent** -> **Image Decision Agent**. Loop if revisions needed.
8.  Orchestrator packages approved text versions and branded visual guides into a "KOL Content Package."

**C. Batch Material Generation (Addressing Sister's Pain Point):**
1.  User defines a product and a set of 3-5 KOL archetypes/platforms.
2.  Orchestrator runs the Planner -> Writer/Image -> Refiner -> Branding chain in parallel or sequentially for each archetype, generating a tailored package for each. This leverages the "multi-version" capability of the Refiner.

## 6. Database Schema Design (Conceptual)

* `Users`: id, email, password_hash, role (agency_user, brand_user, admin)
* `Organizations`: id, name (agency/brand name)
* `User_Organizations`: user_id, organization_id, role_in_org
* `Brands`: id, organization_id, name, brand_guidelines (text, JSON), logo_url
* `Products`: id, brand_id, name_cn, name_en, description_cn, description_en, features (JSON), images_urls
* `Campaigns`: id, brand_id, name, target_market (JSON: country, demo, platform), goals
* `KOL_Profiles_Templates`: id, campaign_id, archetype_name, platform, style_notes (for Planner input)
* `Content_Strategies`: id, campaign_id, kol_profile_template_id, planner_agent_output (JSON: angles, messages)
* `Content_Drafts`: id, content_strategy_id, agent_type (writer, refiner), version, text_content, visual_concept_description, status (draft, pending_review, approved, rejected)
* `Branded_Assets_Concepts`: id, content_draft_id (visual), branding_agent_output (JSON: how logo applied, etc.), image_url_mockup
* `Feedback_Items`: id, content_draft_id, user_id, rating, comments, (for learning loop)
* `Localization_KB_Entries`: id, market_key (e.g., "US_GenZ_TikTok"), insight_type (cultural, trend, language), content (text, embeddings for RAG)

## 7. MVP Development Plan & Phased Rollout

**Goal: Focus on solving your sister's most pressing pain points first.**

* **Phase 0: Deep Dive with Your Sister (As previously discussed)**
    * Confirm MVP scope based on her top 3 pain points.
    * Gather real-world anonymous case data for testing.

* **Phase 1: Core Localized Text Generation & "Micro-Tuner" MVP (Solve "content micro-tuning" & "batch content generation" for text)**
    * **Agents:** Orchestrator (simple), Planner (lite - focus on strategy from structured input, basic RAG from a small, curated KB), Writer, **Refiner (Text Micro-Tuner - this is your star)**, Text Critic (rule-based + simple LLM check), Text Decision.
    * **Features:**
        * Project setup (Brand, Product, basic Target Market/KOL type).
        * Planner generates 1-2 localized angles/core messages.
        * Writer generates draft copy for these angles.
        * **Refiner allows guided micro-tuning & generates 2-3 variations of the approved copy.**
        * Simple review/approval flow.
        * Output: Text-based content package.
    * **Target User:** Your sister.
    * **Goal:** Prove the Text Micro-Tuner is a game-changer for efficiency. Prove AI can generate good localized first drafts.

* **Phase 2: Add Visual Concepts & Basic Branding (Solve "logo application")**
    * **Agents:** Add Image Agent (concept suggestions, not generation initially) and Branding Agent (logo on placeholder/template visuals). Add Image Critic/Decision (manual review initially for MVP).
    * **Features:**
        * Image Agent suggests visual styles/scenes based on approved text and Planner strategy.
        * Branding Agent allows upload of logo and applies it to simple visual template examples.
        * Output: Content package now includes text variations + visual concept guides with branding.
    * **Goal:** Provide a more complete package for KOLs, reduce manual visual briefing.

* **Phase 3: Enhance Planner with Deeper Localization & Batch Processing**
    * **Agents:** Significantly improve Planner's RAG capabilities by expanding the Localization KB. Enhance Orchestrator for batch processing.
    * **Features:**
        * Planner provides more nuanced and diverse strategies.
        * System can take one product and generate content packages for 3-5 different KOL archetypes/platforms in a batch.
    * **Goal:** Address "batch content generation" more robustly and showcase stronger localization.

* **Phase 4: Beta Launch to Select Agencies/Brands**
    * Onboard a few more users (your sister's contacts).
    * Gather broader feedback, collect more data.
    * Refine pricing and onboarding.

* **Phase 5: Expansion & Full Multi-Agent System**
    * Develop Distributor Agent, advanced Trend Radar, etc.
    * AI Image Generation integration.
    * Deeper learning loops.

## 8. Differentiation & Building a Moat

* **Unique Resource & Insight:** Your sister's direct involvement and access to real CBEC cases.
* **Text Micro-Tuner Agent:** This specific feature, if done well, can be a major UX win and differentiator.
* **Deep CBEC Localization Focus:** The Planner Agent + Localization KB, continuously improved, becomes a core asset.
* **Workflow Automation for a Niche:** Solving the *specific end-to-end workflow* for CBEC KOL content is more valuable than generic tools.
* **Data Flywheel (Long-Term):** Aggregated (and anonymized, if applicable) data on what content strategies and micro-tunes work best for specific market/KOL/product combinations can make the system progressively smarter.

## 9. Potential Challenges & Mitigation

* **Complexity:** Multi-agent systems are complex. Start simple, build iteratively.
* **LLM Costs & Latency:** Optimize prompts, use appropriate models, implement caching.
* **Quality of Localization:** Heavy reliance on Planner & KB. Constant curation and updates needed. Human oversight is key, especially initially.
* **Maintaining the Text Micro-Tuner's Effectiveness:** Needs robust prompt engineering and possibly fine-tuning as LLMs evolve.
* **User Adoption:** Focus on clear ROI (time saved, better KOL adoption of materials).

## 10. Future Enhancements

* **Direct KOL Portal:** Allow KOLs to log in, view briefs/materials, provide feedback, or even use a simplified "Refiner" for their contributions.
* **Performance Analytics Integration:** Track effectiveness of content generated via the system (requires KOLs/brands to provide data or platform API access).
* **Automated Trend Integration:** More sophisticated Trend Radar Agent.
* **AI Image/Video Generation:** Fully integrated AI generation for visual assets.
* **Compliance Checks:** AI to flag potential compliance issues for specific markets/platforms.

## 11. Conclusion

You have a strong, defensible starting point due to your unique insights and resources. By focusing on the specific pain points of Chinese brands going global with KOL marketing, and by innovatively using AI agents (especially the Text Micro-Tuner and a smart Planner), you can build a highly valuable platform. An iterative MVP approach, with your sister as the initial super-user, is the right way to begin. Good luck!


## Appendix
* Multi-agents structure Flow:
graph TD
    A["用户输入<br/>产品信息等"] --> PA["Planner Agent<br/>平台分析, 内容大纲<br/>图片要求, 风格指引"];

    PA -- 大纲与文本要求 --> WA["Writer Agent<br/>撰写初稿文案"];
    WA -- 初稿文案 --> RA["Refiner Agent<br/>文案微调 + 多版本输出"];
    RA -- 优化后文案版本 --> TCA["Text Critic Agent<br/>文案审核"];
    TCA -- 审核意见 --> TDA{"Text Decision Agent<br/>判断是否通过"};
    TDA -- "不通过 (Needs Revision)" --> RA;
    TDA -- "通过 (Pass)" --> ApprovedText["已批准的文案版本"];

    PA -- 图片要求与风格指引 --> IA["Image Agent<br/>(生成/建议图片概念或草图)"];
    IA -- 图片概念/草图 --> BA["Branding Agent<br/>(图片加Logo/字体/色调等)"];
    BA -- 带品牌元素的图片 --> ICA["Image Critic Agent<br/>图片审核"];
    ICA -- 审核意见 --> IDA{"Image Decision Agent<br/>判断是否通过"};
    IDA -- "不通过 (Needs Revision)" --> BA;
    IDA -- "通过 (Pass)" --> ApprovedImages["已批准的品牌图片"];

    ApprovedText --> ASSM["内容整合与打包<br/>(Content Assembly & Packaging)"];
    ApprovedImages --> ASSM;

    ASSM -- 最终内容包 --> DA["Distributor Agent<br/>多平台分发"];
    DA --> POSTED["内容发布成功"];

    %% Optional: Show Orchestrator if you want to explicitly visualize it
    %% For a cleaner diagram focused on agent functions, the Orchestrator can be implied
    %% as managing these transitions. If you add it:
    %% O[Orchestrator Agent]
    %% A --> O
    %% O --> PA
    %% PA --> O
    %% O --> WA ... and so on for every step.
    %% This can make the diagram very busy, so it's often omitted for clarity on agent roles.