from unreal import(
    AssetToolsHelpers,
    EditorAssetLibrary,
    AssetTools,
    Material,
    MaterialFactoryNew,
    MaterialEditingLibrary,
    MaterialExpressionTextureSampleParameter2D as TexSample2D,
    MaterialProperty,
    AssetImportTask,
    FbxImportUI ## imports all the important items for this script
)

import os

class UnrealUtility:
    def __init__(self):
        self.substanceRootDir='/game/Substance/' #defines the root directory
        self.substanceBaseMatName = 'M_SubstanceBase' # defines the base material from substance
        self.substanceBaseMatPath = self.substanceRootDir + self.substanceBaseMatName # defines the path the material needs to take using the root directory 
        self.substanceTempFolder='/game/Substance/temp'  # creates a temp file
        self.baseColorName = "BaseColor" #defines the base color from substance
        self.normalName = "Normal" # defines the normal map
        self.occRoughnessMetallic = "OcclusionRoughnessMetallic" # defines the ORM map

    def GetAssetTools(self)->AssetTools:
       return AssetToolsHelpers.get_asset_tools() # returns the asset tool helper to allow it to work
    
    def ImportFromDir(self, dir): # defines a class called ImportFromDir, which will import from the directory
        for file in os.listdir(dir): # checks for a file in the listed directory
            if ".fbx" in file: # checks for any .fbx files in the file
                self.LoadMeshFromPath(os.path.join(dir, file)) # loads the .fbx into the proper file/project

    def LoadMeshFromPath(self, meshPath):
        meshName = os.path.split(meshPath)[-1].replace(".fbx", " ")
        importTask = AssetImportTask() # sets imports tasts to the name of importTask
        importTask.replace_existing = True
        importTask.filename = meshPath
        importTask.destination_path = '/game/' + meshName # sets the destination paths of the .fbx files to a new path under /game/
        importTask.automated = True
        importTask.save = True # saves and autosaves all thats been done so far

        fbxImportOption = FbxImportUI()
        fbxImportOption.import_mesh = True
        fbxImportOption.import_as_skeletal = False
        fbxImportOption.import_materials = False
        fbxImportOption.static_mesh_import_data.combine_meshes = True
        importTask.options = fbxImportOption

        self.GetAssetTools().import_asset_tasks([importTask])
        return importTask.get_objects()[0]

    def FindOrBuildBaseMaterial(self):
        if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath):
            return EditorAssetLibrary.load_asset(self.substanceBaseMatPath)
        
        baseMat = self.GetAssetTools().create_asset(self.substanceBaseMatName, self.substanceRootDir, Material, MaterialFactoryNew())
        basecolor = MaterialEditingLibrary.create_material_expression(baseMat,TexSample2D, - 800, 0 ) # sets unreal nodes at a certain point in the grid
        basecolor.set_editor_property("parameter_name", self.baseColorName) #names the base color
        MaterialEditingLibrary.connect_material_property(basecolor, "RGB", MaterialProperty.MP_BASE_COLOR) # sets the base color map under the "rgb" channel

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400) # sets unreal nodes at a certain point in the grid
        normal.set_editor_property("parameter_name", self.normalName) # names the normal map
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal")) # loads the texture of the normal map
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL) # sets the normal map under the "rgb" channel

        occRoughnessMetallic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800) # sets unreal nodes at a certain point in the grid
        occRoughnessMetallic.set_editor_property("parameter_name", self.occRoughnessMetallic) # names the ORM map
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION) # sets the ao map under the "r" channel
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "G", MaterialProperty.MP_ROUGHNESS) # sets the roughness map under the "g" channel
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "B", MaterialProperty.MP_METALLIC) # sets the metallic map under the "b" channel

        EditorAssetLibrary.save_asset(baseMat.get_path_name())
        return baseMat