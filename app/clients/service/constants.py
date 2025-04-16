COLUMNS_FIELDS = [
    "age",  # Client's age
    "gender",  # Client's gender (bool)
    "work_experience",  # Years of work experience
    "canada_workex",  # Years of work experience in Canada
    "dep_num",  # Number of dependents
    "canada_born",  # Born in Canada
    "citizen_status",  # Citizenship status
    "level_of_schooling",  # Highest level achieved (1-14)
    "fluent_english",  # English fluency scale (1-10)
    "reading_english_scale",  # Reading ability scale (1-10)
    "speaking_english_scale",  # Speaking ability scale (1-10)
    "writing_english_scale",  # Writing ability scale (1-10)
    "numeracy_scale",  # Numeracy ability scale (1-10)
    "computer_scale",  # Computer proficiency scale (1-10)
    "transportation_bool",  # Needs transportation support (bool)
    "caregiver_bool",  # Is primary caregiver (bool)
    "housing",  # Housing situation (1-10)
    "income_source",  # Source of income (1-10)
    "felony_bool",  # Has a felony (bool)
    "attending_school",  # Currently a student (bool)
    "currently_employed",  # Currently employed (bool)
    "substance_use",  # Substance use disorder (bool)
    "time_unemployed",  # Years unemployed
    "need_mental_health_support_bool",  # Needs mental health support (bool)
]

BOOL_FIELDS = [
    "canada_born", "citizen_status", "fluent_english",
    "transportation_bool", "caregiver_bool", "felony_bool",
    "attending_school", "currently_employed", "substance_use",
    "need_mental_health_support_bool"
]

INTERVENTION_FIELDS = [
    "employment_assistance", "life_stabilization", "retention_services",
    "specialized_services", "employment_related_financial_supports",
    "employer_financial_supports", "enhanced_referrals"
]

INTERVENTION_NAMES = {
    "employment_assistance": "General Employment Assistance Services",
    "life_stabilization": "Life Stabilization Services",
    "retention_services": "Retention Services",
    "specialized_services": "Specialized Services",
    "employment_related_financial_supports":\
        "Employment-Related Financial Supports for Job Seekers and Employers",
    "employer_financial_supports": "Employer Financial Supports",
    "enhanced_referrals": "Enhanced Referrals for Skills Development"
}

FIELDS_WITH_LOW_AT_ONE = {"level_of_schooling", "housing", "income_source"}

DEFAULT_INTERVENTION_COMBINATIONS = [
    {"employer_financial_supports": True},
    # Combination 1
    {
        "retention_services": True,
        "enhanced_referrals": True
    },

    # Combination 2
    {
        "retention_services": True,
        "employment_related_financial_supports": True,
        "enhanced_referrals": True
    },
    # Combination 3
    {
        "employment_assistance": True,
        "retention_services": True,
        "employment_related_financial_supports": True,
        "enhanced_referrals": True
    }
]
