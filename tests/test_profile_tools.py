from agent_under_hood.tools.profile import get_contact_info, list_projects


def test_get_contact_info_returns_email_linkedin_github():
    info = get_contact_info.invoke({})
    assert set(info.keys()) == {"email", "linkedin", "github"}


def test_list_projects_returns_name_and_summary_per_project():
    projects = list_projects.invoke({})
    assert len(projects) > 0
    for project in projects:
        assert "name" in project
        assert "summary" in project
