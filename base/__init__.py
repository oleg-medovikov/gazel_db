from .base                           import metadata, engine, database
from .users                          import table_users
from .users_log                      import table_users_log
from .projects                       import table_projects
from .projects_access                import table_project_access
from .projects_reference             import table_projects_reference
from .projects_reference_description import table_projects_reference_description
from .objects                        import table_objects
from .objects_binary                 import objects_binary

metadata.create_all(engine)
