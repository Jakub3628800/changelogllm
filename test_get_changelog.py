import subprocess

def test_requests_changelog():
    """Test that we can get changelog for requests package"""
    result = subprocess.run(
        ['python', 'get_changelog.py', 'requests'],
        capture_output=True,
        text=True
    )
    
    # Check that the command succeeded
    assert result.returncode == 0
    
    # Check that we got some output
    assert len(result.stdout) > 0
    
    # Check for some expected content in the output
    assert 'requests' in result.stdout.lower()
    
    # Check that it's not an error message
    assert 'error' not in result.stdout.lower()