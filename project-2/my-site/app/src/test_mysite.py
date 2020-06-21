import unittest

from mysite import app

class BasicTestCase(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    def test_healthcheck(self):
        tester = app.test_client(self)
        response = tester.get('/healthcheck', content_type='html/txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'SITE IS UP')

if __name__ == '__main__':
    unittest.main()