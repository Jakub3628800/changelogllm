import subprocess
import unittest

class TestGetChangelog(unittest.TestCase):
    def test_requests_changelog(self):
        """Test that we can get changelog for requests package"""
        result = subprocess.run(
            ['python', 'get_changelog.py', 'requests'],
            capture_output=True,
            text=True
        )
        
        # Check that the command succeeded
        self.assertEqual(result.returncode, 0)
        
        # Check that we got some output
        self.assertTrue(len(result.stdout) > 0)
        
        # Check for some expected content in the output
        self.assertIn('requests', result.stdout.lower())
        
        # Check that it's not an error message
        self.assertNotIn('error', result.stdout.lower())

if __name__ == '__main__':
    unittest.main()