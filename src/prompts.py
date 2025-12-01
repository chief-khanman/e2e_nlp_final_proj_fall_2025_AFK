from langchain_core.prompts import PromptTemplate

# System prompt for IEP goal generation
SYSTEM_PROMPT = """You are an expert special education professional specializing in creating Individualized Education Program (IEP) goals for students with disabilities. Your role is to generate appropriate, measurable postsecondary goals and short-term objectives that align with:

1. Industry standards from the Occupational Outlook Handbook
2. Educational standards (21st Century Skills and Employability Skills)
3. IDEA 2004 requirements for transition planning

You have access to relevant information about occupations, educational standards, and IEP best practices through the provided context. Use this information to create goals that are:

- Measurable and specific
- Aligned with the student's interests and abilities
- Connected to industry and educational standards
- Compliant with IDEA 2004 requirements
- Realistic and achievable within the specified timeframe
"""

# Prompt for generating postsecondary goals
POSTSECONDARY_GOALS_PROMPT = PromptTemplate(
    input_variables=["student_info", "context"],
    template="""Based on the following student information and relevant context, generate appropriate measurable postsecondary goals.

Student Information:
{student_info}

Relevant Context (Occupational Data, Standards, and Best Practices):
{context}

Generate the following postsecondary goals:

1. EMPLOYMENT GOAL: A specific, measurable employment goal that aligns with the student's interests and abilities.

2. EDUCATION/TRAINING GOAL: A specific goal for post-high school education or training that supports the employment goal.

3. INDEPENDENT LIVING GOAL (if appropriate): A goal related to independent living skills.

For each goal:
- Make it specific and measurable
- Include the timeframe ("After high school")
- Connect it to the student's interests and assessment results
- Ensure it aligns with realistic career opportunities

Format your response as:

EMPLOYMENT GOAL:
[Your goal here]

EDUCATION/TRAINING GOAL:
[Your goal here]

INDEPENDENT LIVING GOAL:
[Your goal here, or "Not applicable" if not needed]
"""
)

# Prompt for generating annual goals
ANNUAL_GOAL_PROMPT = PromptTemplate(
    input_variables=["student_info", "postsecondary_goals", "context"],
    template="""Based on the student information, postsecondary goals, and relevant context, generate a measurable annual goal that will help the student progress toward their postsecondary goals.

Student Information:
{student_info}

Postsecondary Goals:
{postsecondary_goals}

Relevant Context (Standards and Skills):
{context}

Generate ONE comprehensive annual goal that:
- Is measurable with clear criteria for success
- Includes a specific timeframe (e.g., "In 36 weeks")
- Aligns with educational standards and employability skills
- Supports the student's postsecondary employment goal
- Specifies the context where the skill will be demonstrated
- Includes measurable criteria (e.g., "in 4 out of 5 opportunities")

Then, identify which standards this goal aligns with:
- Occupational Outlook Handbook requirements
- 21st Century Skills
- Employability Skills

Format your response as:

ANNUAL GOAL:
[Your measurable annual goal here]

ALIGNMENT TO STANDARDS:
- Occupational Outlook Handbook: [Specific requirements this goal addresses]
- 21st Century Skills: [Specific skills this goal develops]
- Employability Skills: [Specific employability skills this goal targets]
"""
)

# Prompt for generating short-term objectives
SHORT_TERM_OBJECTIVES_PROMPT = PromptTemplate(
    input_variables=["student_info", "annual_goal", "context"],
    template="""Based on the student information, annual goal, and relevant context, generate 4 short-term objectives (benchmarks) that break down the annual goal into smaller, sequential steps.

Student Information:
{student_info}

Annual Goal:
{annual_goal}

Relevant Context:
{context}

Generate 4 short-term objectives that:
- Progress sequentially from less to more independent
- Build on each other toward the annual goal
- Are measurable with clear criteria
- Include specific timeframes (by quarter or date)
- Move from controlled settings to more natural environments
- Follow a logical progression (e.g., role-play → simulated settings → community-based instruction → work-based learning)

Format your response as:

SHORT-TERM OBJECTIVE 1 (First Quarter):
[Objective with criterion]

SHORT-TERM OBJECTIVE 2 (Second Quarter):
[Objective with criterion]

SHORT-TERM OBJECTIVE 3 (Third Quarter):
[Objective with criterion]

SHORT-TERM OBJECTIVE 4 (Fourth Quarter):
[Objective with criterion]
"""
)

# Prompt for explaining alignment and connections
EXPLANATION_PROMPT = PromptTemplate(
    input_variables=["student_info", "postsecondary_goals", "annual_goal", "objectives", "context"],
    template="""Based on all the generated IEP components, provide a clear explanation of how everything connects together.

Student Information:
{student_info}

Postsecondary Goals:
{postsecondary_goals}

Annual Goal:
{annual_goal}

Short-term Objectives:
{objectives}

Relevant Context:
{context}

Provide a clear, concise explanation that addresses:

1. How the postsecondary goals align with the student's interests and assessment results
2. How the annual goal supports the postsecondary employment goal
3. How the goals connect to specific industry requirements from the Occupational Outlook Handbook
4. How the goals align with educational standards (21st Century Skills and Employability Skills)
5. How the short-term objectives provide a logical progression toward the annual goal

Keep your explanation clear and organized. Use specific examples from the goals and standards.

Format your response in clear sections.
"""
)

# Combined prompt for generating complete IEP
COMPLETE_IEP_PROMPT = PromptTemplate(
    input_variables=["student_name", "age", "grade", "disability", "interests", "assessment_results", "context"],
    template="""You are an expert special education professional. Based on the student information and relevant context, generate a complete set of IEP transition goals.

STUDENT INFORMATION:
Name: {student_name}
Age: {age}
Grade: {grade}
Disability: {disability}
Interests: {interests}
Assessment Results: {assessment_results}

RELEVANT CONTEXT (Career Information, Standards, and Best Practices):
{context}

Generate a complete IEP transition plan including:

1. MEASURABLE POSTSECONDARY GOALS
   - Employment Goal
   - Education/Training Goal
   - Independent Living Goal (if appropriate)

2. MEASURABLE ANNUAL GOAL
   - Include timeframe, specific skill, context, and criteria for success
   - Ensure it aligns with and supports the postsecondary goals

3. ALIGNMENT TO STANDARDS
   - Specific Occupational Outlook Handbook requirements
   - Relevant 21st Century Skills
   - Relevant Employability Skills

4. SHORT-TERM OBJECTIVES/BENCHMARKS
   - Four sequential objectives that build toward the annual goal
   - Include timeframes and measurable criteria
   - Show progression from structured to natural settings

5. EXPLANATION OF CONNECTIONS
   - How goals align with student's interests and needs
   - How goals connect to industry and educational standards
   - How objectives support goal achievement

Make all goals and objectives:
- Specific and measurable
- Appropriate for the student's age and disability
- Aligned with the student's interests
- Connected to realistic career opportunities
- Compliant with IDEA 2004 requirements

Format your response with clear section headers and organized content.
"""
)

# Prompt for handling missing information
CLARIFICATION_PROMPT = PromptTemplate(
    input_variables=["student_info", "missing_info"],
    template="""The following student information is incomplete:

Provided Information:
{student_info}

Missing Information:
{missing_info}

Please note what information is missing and proceed to generate IEP goals with the following approach:
1. Use the available information to generate appropriate goals
2. Make reasonable assumptions based on typical student profiles with similar characteristics
3. Clearly note in your response what assumptions were made
4. Suggest what additional assessments or information would be helpful

Proceed with generating the IEP components based on available information.
"""
)
