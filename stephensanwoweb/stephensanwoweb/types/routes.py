from enum import Enum

class Routes(str, Enum):
    index = ""
    profile = "profile"
    projects = "projects"
    blog = "blog"
    ai_playground = "ai-playground"

class BackendRoutes(str, Enum):
    admin = "admin"
    login = "login"
    auth = "auth"
    dashboard = "dashboard"
    blog = "dashboard/blog"
    create_blog = "dashboard/blog/create"
    publish_blog = "dashboard/blog/publish"
    delete_blog = "dashboard/blog/delete"
    unpublish_blog = "dashboard/blog/unpublish"

class ProjectRoutes(str, Enum):
    openworkflow = "projects/open-workflow-v0.1"
    project_corpenicus = "projects/project-corpenicus-v1.2"
    ai_chatbot = "projects/ai-chatbot"
    kpmg_propjects = "projects/kpmg-projects"
