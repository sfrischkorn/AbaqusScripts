import abaqusConstants

class Mesh(object):
    elem_shape = None
    technique = None
    algorithm = None
    min_transition = None
    size_growth = None
    allow_mapped = None

    def __init__(self, elem_shape=None, technique=None, algorithm=None, min_transition=None, size_growth=None, allow_mapped=None):
        assert elem_shape is None or elem_shape in [abaqusConstants.QUAD, abaqusConstants.QUAD_DOMINATED,
                                                    abaqusConstants.TRI, abaqusConstants.HEX,
                                                    abaqusConstants.HEX_DOMINATED, abaqusConstants.TET,
                                                    abaqusConstants.WEDGE] , \
            "elem_shape must be one of %s" % 'QUAD, QUAD_DOMINATED, TRI, HEX, HEX_DOMINATED, TET, or WEDGE'

        assert technique is None or technique in [abaqusConstants.FREE, abaqusConstants.STRUCTURED,
                                                  abaqusConstants.SWEEP, abaqusConstants.BOTTOM_UP,
                                                  abaqusConstants.SYSTEM_ASSIGN] , \
            "technique must be one of %s" % 'FREE, STRUCTURED, SWEEP, BOTTOM-UP, or SYSTEM_ASSIGN'

        if technique == abaqusConstants.FREE:
            if elem_shape == abaqusConstants.QUAD or elem_shape == abaqusConstants.QUAD_DOMINATED:
                assert algorithm is None or algorithm in [abaqusConstants.MEDIAL_AXIS, abaqusConstants.ADVANCING_FRONT], \
                    "For FREE QUAD or QUAD_DOMINATED meshing, only MEDIAL_AXIS or ADVANCING_FRONT are valid"
            elif elem_shape == abaqusConstants.TET:
                assert algorithm is None or algorithm == abaqusConstants.NON_DEFAULT, \
                    "For free tetragonal meshing, only NON_DEFAULT is valid"
            else:
                assert algorithm is None, \
                    "Invalid algorithm. Valid values are: For free quad or quad dominated: MEDIAL_AXIS or " \
                    "ADVANCING_FRONT; for free tetragonal: NON_DEFAULT; for sweep hexagonal or hex dominated: " \
                    "MEDIAL_AXIS or ADVANCING_FRONT. For other meshes, algorithm should be None"
        elif technique == abaqusConstants.SWEEP:
            if elem_shape == abaqusConstants.HEX or elem_shape == abaqusConstants.HEX_DOMINATED:
                assert algorithm is None or algorithm in [abaqusConstants.MEDIAL_AXIS, abaqusConstants.ADVANCING_FRONT], \
                    "For FREE HEX or HEX_DOMINATED meshing, only MEDIAL_AXIS or ADVANCING_FRONT are valid"
            else:
                assert algorithm is None, "Invalid algorithm. Valid values are: For free quad or quad dominated: " \
                                          "MEDIAL_AXIS or ADVANCING_FRONT; for free tetragonal: NON_DEFAULT; for " \
                                          "sweep hexagonal or hex dominated: MEDIAL_AXIS or ADVANCING_FRONT. For other meshes, algorithm should be None"
        else:
            assert algorithm is None, "Invalid algorithm. Valid values are: For free quad or quad dominated: " \
                                      "MEDIAL_AXIS or ADVANCING_FRONT; for free tetragonal: NON_DEFAULT; for sweep " \
                                      "hexagonal or hex dominated: MEDIAL_AXIS or ADVANCING_FRONT. For other meshes, " \
                                      "algorithm should be None"
        
        if not (((technique == abaqusConstants.FREE and elem_shape == abaqusConstants.QUAD) or
                     (technique == abaqusConstants.SWEEP and elem_shape == abaqusConstants.HEX)) and
                        algorithm == abaqusConstants.MEDIAL_AXIS) or (technique == abaqusConstants.STRUCTURED
                                                                                 and elem_shape == abaqusConstants.QUAD):
            assert min_transition is None, "min_transition may only be set for Free quadrilateral meshing or " \
                                           "hexahedral sweep meshing with algorithm=MEDIAL_AXIS, or Structured " \
                                           "quadrilateral meshing"

        if elem_shape == abaqusConstants.TET:
            assert size_growth is None or size_growth in [abaqusConstants.MODERATE, abaqusConstants.MAXIMUM], \
                "The valid values of size_growth for tetrahedral meshes are MODERATE or MAXIMUM"
        else:
            assert size_growth is None, "size_growth may only be set for tetrahedral meshes"

        if not ((technique == abaqusConstants.FREE and
                     (elem_shape in [abaqusConstants.TRI, abaqusConstants.TET] or
                          (elem_shape in [abaqusConstants.QUAD, abaqusConstants.QUAD_DOMINATED] and
                                   algorithm == abaqusConstants.ADVANCING_FRONT))) or
                    (technique == abaqusConstants.SWEEP and elem_shape in [abaqusConstants.HEX,
                                                                           abaqusConstants.HEX_DOMINATED] and
                             algorithm == abaqusConstants.ADVANCING_FRONT)):
            assert allow_mapped is None, "allow_mapped can only be set in the following cases: Free triangular " \
                                         "meshing; Free quadrilateral or quadrilateral-dominated meshing with " \
                                         "algorithm=ADVANCING_FRONT; Hexahedral or hexahedral-dominated sweep meshing " \
                                         "with algorithm=ADVANCING_FRONT; Free tetrahedral meshing. allowMapped=True " \
                                         "implies that mapped triangular meshing can be used on faces that bound three-dimensional regions."

        self.elem_shape = elem_shape
        self.technique = technique
        self.algorithm = algorithm
        self.min_transition = min_transition
        self.size_growth = size_growth
        self.allow_mapped = allow_mapped

    def GenerateCommand(self, regions):
        commands = []
        if self.elem_shape:
            commands.append("elemShape={0}".format(self.elem_shape))

        if self.technique:
            commands.append("technique='{0}'".format(self.technique))

        if self.algorithm:
            commands.append("algorithm='{0}'".format(self.algorithm))

        if self.min_transition:
            commands.append("minTransition='{0}'".format(self.min_transition))

        if self.size_growth:
            commands.append("sizeGrowth='{0}'".format(self.size_growth))

        if self.allow_mapped:
            commands.append("allowMapped='{0}'".format(self.allow_mapped))

        if len(commands) > 0:
            cmd =  ", ".join(commands)
            return "p.setMeshControls(regions={0}, {1})".format(regions, cmd) 
        else:
            return "p.setMeshControls(regions={0})".format(regions) 
