"""
Define materials for abaqus. To create a new material, define the class for it, and add an entry to the materials enum with the value
set to the name of the material class. The Elastic class provides a good template to follow. The youngs_modulus and poissons_ratio would need
to be changed for the variables of the new material.
"""

def enum(**enums):
    return type('Enum', (), enums)

materials = enum(ELASTIC='Elastic')

class MaterialFactory:
    """
    Factory class to encapsulate creation of materials. Using **kwargs lets you
    pass values to the material constructors,
    eg. for an Elastic material createMaterial(materials.ELASTIC, name="mat",
        youngs_modulus = 20000, poissons_ratio = 2)
    """

    factories = {}

    def addFactory(material, materialFactory):
        MaterialFactory.factories.put[material] = materialFactory

    # A Template Method:
    def createMaterial(material, **kwargs):
        if not material in MaterialFactory.factories:
            MaterialFactory.factories[material] = eval(material + '.Factory()')
        return MaterialFactory.factories[material].create(**kwargs)

    addFactory = staticmethod(addFactory)
    createMaterial = staticmethod(createMaterial)


class Material(object):
    name = ""

    def __init__(self, name):
        self.name = name

    def generate_material(self, model_name):
        return "{0}.Material(name='{1}')".format(model_name, self.name)

    def generate_section_command(self, model_name, section_name):
        return "{0}.HomogeneousSolidSection(material='{1}', name='{2}', thickness=None)".format(model_name, self.name, section_name)


class Elastic(Material):
    youngs_modulus = 0.0
    poissons_ratio = 0.0

    def __init__(self, name, youngs_modulus, poissons_ratio):
        super(Elastic, self).__init__(name)

        self.youngs_modulus = youngs_modulus
        self.poissons_ratio = poissons_ratio

    def generate_material_commands(self, model_name, section_name):
        parent = super(Elastic, self)

        commands = []
        commands.append(parent.generate_material(model_name))
        commands.append("{0}.materials['{1}'].Elastic(table=(({2}, {3}), ))".format(model_name, self.name, self.youngs_modulus, self.poissons_ratio))
        commands.append(parent.generate_section_command(model_name, section_name))

        return commands

    def __str__(self):
        return "Elastic: Name; {0}, Young's Modulus: {1}, Poisson's Ratio: {2}".format(self.name, self.youngs_modulus, self.poissons_ratio)


    class Factory:
        def create(self, **kwargs):
            return Elastic(**kwargs)
