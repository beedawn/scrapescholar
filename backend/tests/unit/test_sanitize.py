from academic_databases.Scopus.scopus import sanitize_link_scopus


# Test Case 22.1 - Safe link
def test_safe_link():
    link = "https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85195248704&origin=inward"
    sanitized_link = sanitize_link_scopus(link)
    assert sanitized_link == link


# Test Case 22.2
def test_failed_scheme():
    link = "http://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85195248704&origin=inward"
    sanitized_link = sanitize_link_scopus(link)
    assert sanitized_link == "Potentially malicious link detected. Blocked for user safety."


#Test Case 22.3
def test_failed_netloc():
    link = "https://scammer.site.com/inward/record.uri?partnerID=HzOxMe3b&scp=85195248704&origin=inward"
    sanitized_link = sanitize_link_scopus(link)
    assert sanitized_link == "Potentially malicious link detected. Blocked for user safety."
