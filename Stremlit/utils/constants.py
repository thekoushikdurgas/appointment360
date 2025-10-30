"""
Constants
"""
from enum import Enum


class ExportScope(Enum):
    SELECTED = "selected"
    CURRENT_PAGE = "current_page"
    FILTERED = "filtered"
    ALL = "all"


class ExportFormat(Enum):
    EXCEL = "excel"
    CSV = "csv"


# Industry list
INDUSTRIES = [
    "Technology", "Healthcare", "Finance", "Education", "Retail",
    "Manufacturing", "Real Estate", "Transportation", "Energy", "Media",
    "Telecommunications", "Hospitality", "Food & Beverage", "Construction",
    "Agriculture", "Automotive", "Consulting", "Legal", "Marketing",
    "Insurance", "Non-profit", "Government", "Other"
]

# Countries (most common)
COUNTRIES = [
    "United States", "United Kingdom", "Canada", "Australia", "Germany",
    "France", "Italy", "Spain", "Netherlands", "Belgium", "Sweden",
    "Norway", "Denmark", "Finland", "Switzerland", "Austria",
    "Poland", "India", "China", "Japan", "South Korea", "Singapore",
    "United Arab Emirates", "Brazil", "Mexico", "Argentina", "Chile", "Other"
]

# Company sizes
COMPANY_SIZES = [
    "1-10", "11-50", "51-200", "201-500", "501-1000",
    "1001-5000", "5001-10000", "10000+"
]

# Revenue ranges
REVENUE_RANGES = [
    "$0 - $1M", "$1M - $10M", "$10M - $50M", "$50M - $100M",
    "$100M - $500M", "$500M - $1B", "$1B+"
]
