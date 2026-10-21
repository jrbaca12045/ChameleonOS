---
name: lead_research
description: "Identifies high-quality leads for a product or service by analyzing the business, searching for target companies, and providing actionable contact strategies. Use for sales prospecting, business development, and marketing outreach."
triggers: lead research, find leads, prospect list, sales leads, b2b leads, target companies, find prospects
---

# Lead Research

This skill helps identify and qualify potential leads for a business by analyzing the product or service, understanding the ideal customer profile, and providing actionable outreach strategies.

## When to Use This Skill

- Finding potential customers or clients for a product or service
- Building a list of companies to reach out to for partnerships
- Identifying target accounts for sales outreach
- Researching companies that match an ideal customer profile
- Preparing for business development activities

## What This Skill Does

1. **Understands the business** - Analyzes product/service, value proposition, and target market
2. **Identifies target companies** - Finds companies matching the ideal customer profile based on industry, size, location, tech stack, growth stage, and pain points
3. **Prioritizes leads** - Ranks companies based on fit score and relevance
4. **Provides contact strategies** - Suggests how to approach each lead with personalized messaging
5. **Enriches data** - Gathers relevant information about decision-makers and company context

## How to Use

### Basic Usage

Describe your product/service and what you are looking for:

    I am building [product description]. Find me 10 companies in [location/industry]
    that would be good leads for this.

### With Your Codebase

Run this from your product source code directory for better results:

    Look at what I am building in this repository and identify the top 10 companies
    in [location/industry] that would benefit from this product.

### Advanced Usage

For more targeted research:

    My product: [description]
    Ideal customer profile:
    - Industry: [industry]
    - Company size: [size range]
    - Location: [location]
    - Current pain points: [pain points]
    - Technologies they use: [tech stack]

    Find me 20 qualified leads with contact strategies for each.

## Instructions

When a user requests lead research:

1. **Understand the product/service**
   - If in a code directory, analyze the codebase to understand the product
   - Ask clarifying questions about the value proposition
   - Identify key features and benefits
   - Understand what problems it solves

2. **Define ideal customer profile**
   - Determine target industries and sectors
   - Identify company size ranges
   - Consider geographic preferences
   - Understand relevant pain points
   - Note any technology requirements

3. **Research and identify leads**
   - Search for companies matching the criteria
   - Look for signals of need (job postings, tech stack, recent news)
   - Consider growth indicators (funding, expansion, hiring)
   - Identify companies with complementary products/services
   - Check for budget indicators

4. **Prioritize and score**
   - Create a fit score (1-10) for each lead
   - Consider alignment with ICP, signals of immediate need, budget availability, competitive landscape, timing indicators

5. **Provide actionable output**

   For each lead, provide:
   - Company name and website
   - Why they are a good fit (specific reasons)
   - Priority score (1-10 with explanation)
   - Decision maker role/title to target
   - Contact strategy (personalized approach)
   - Value proposition for them
   - Conversation starters
   - LinkedIn URL if available

6. **Format the output**

   Present results as a scannable markdown report: summary (total leads, priority bands, average fit), then one section per lead with all fields from step 5.

7. **Offer next steps**
   - Suggest saving results to a CSV for CRM import
   - Offer to draft personalized outreach messages
   - Recommend prioritization based on timing
   - Suggest follow-up research for top leads

## Examples

### Example 1: Developer Tool

**User**: I am building a tool that masks sensitive data in AI coding assistant queries. Find potential leads.

**Output**: A prioritized list of companies that use AI coding assistants, handle sensitive data (fintech, healthcare, legal), have evidence in their GitHub repos of using coding agents, may have accidentally exposed sensitive data, and includes LinkedIn URLs of relevant decision-makers.

### Example 2: Local Business

**User**: I run a consulting practice for remote team productivity. Find me 10 companies in the Bay Area that recently went remote.

**Output**: Companies that recently posted remote job listings, announced remote-first policies, are hiring distributed teams, show signs of remote work challenges, with personalized outreach strategies for each.

## Tips for Best Results

- Be specific about your product and its unique value
- Run from your codebase if applicable for automatic context
- Provide context about your ideal customer profile
- Specify constraints like industry, location, or company size
- Request follow-up research on promising leads for deeper insights

## Related Use Cases

- Drafting personalized outreach emails after identifying leads
- Building a CRM-ready CSV of qualified prospects
- Researching specific companies in detail
- Analyzing competitor customer bases
- Identifying partnership opportunities

## Related

- writing/email_drafting/SKILL.md - for drafting the outreach emails
- meta/browsing/SKILL.md - for the fetch-and-save loop this skill uses