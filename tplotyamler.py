"""Create a yaml document out of a dictionary.

The information related to any process running in the system are parsed
out as a dictionary. These are yet to be converted to be yaml documents
to be sent out.
"""

import yaml


class ProcYaml(yaml.YAMLObject):
    """ProcYaml class for creating yaml doc from dictionaries.
    """

    yaml_header = u'!ProcYaml'
    namespace = {}

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.yml = None

    def __repr__(self):
        return '{k}({v})'.format(
            k=self.__class__.__name__,
            v=', '.join(
                ['='.join(
                    [str(item)
                     for item in item]) for item in self.__dict__.items()]))

    def write_to_yaml(self, tag_name):
        """write_to_yaml method of ProcYaml class.

        Takes the dict which is initialized in the object as
        argument. Stores the dict as a yaml document in the yml
        attribute.
        """
        self.namespace[tag_name] = type(
            tag_name,
            (ProcYaml,),
            {'yaml_header': u'!{n}'.format(n=tag_name)})
        self.yml = yaml.dump([self.namespace[tag_name](**self.__dict__)],
                             default_flow_style=False)

    def read_from_yaml(self, yml):
        """read_from_yaml method of ProcYaml class.

        Takes the yaml document as argument and stores the resulting
        dict in the yml attribute of the class.
        """
        self.yml = yaml.load(yml)
