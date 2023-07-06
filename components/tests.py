"""Test GraphQL Interface for speed and functionality."""
from time import time

# import numpy as np
from django.test import TestCase


query = """
{
  components(first: 100) {
    totalCount
    edges {
      node {
        id
        autogenerateDescription
        autogenerateValue
        description
        library {
          id
          ref
        }
        created
        creator {
          id
          username
          email
        }
        lastModified
        lastModifier {
          id
          username
          email
        }
        links {
          totalCount
        }
        lifecycleState {
          id
          name
        }
        manufacturer {
          id
          name
        }
        mpn
        mounting {
          id
          name
        }
        package {
          id
          name
        }
        remarks
        reviews {
          totalCount
        }
        stock
        value
        x
        y
        z
        qualifications {
          totalCount
        }
        fNodes {
          totalCount
        }
        type {
          id
          name
        }
      }
    }
  }
}
"""


class GraphQLSpeedTests(TestCase):
    """Test case that bothers about the speed of GraphQL queries and mutations."""
    # fixtures = ['db.json']
    
    def test_components_speed(self) -> None:
        """This test evaluates the speed of a common GraphQL query."""
        from .schema import schema
        start = time()
        res = schema.execute_sync(query)
        stop = time()

        print(f'Elapsed time for query: {stop - start}s')

        self.assertTrue(len(res.data['components']['edges']) == 100)
        
   