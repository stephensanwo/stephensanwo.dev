from enum import Enum


class Routes(str, Enum):
    index = ""
    profile = "profile"
    projects = "projects"
    blog = "blog"
    ai_playground = "ai-playground"
