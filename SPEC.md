## Pseudo-source specification

The modding community for *The Legend of Zelda: Breath of the Wild* encountered two problems. Firstly, mod creators were spending large amounts of time unpacking and repacking archives, and converting file formats. These tasks could be automated to save time. Secondly, mod users were encountering many mods containing files that were incompatible with each other. Many of these files could be merged to be made compatible, but this merging process required the skills and knowledge of a mod creator.

In order to attempt to solve both of these problems, this document defines an alternative structure for BotW's ROM content files, intending to more closely resemble a set of source files.

### Excluded resources

Resources that have one of the following path prefixes are excluded from the pseudo-source tree:

* Camera/
* Effect/
* ELink2/
* Env/
* Font/
* Game/
* Layout/
* Model/
* Movie/
* NavMesh/
* Physics/
* Shader/
* SLink2/
* Sound/
* System/
* Terrain/
* UI/
* Voice/

Exceptions: `System/Version.txt` and `System/AocVersion.txt` must be included if they exist in the source ROM.

### Structure

The pseudo-source structure is identical to Nintendo's official ROM builds, with the following changes to:

#### Resource packs

All resource packs are extracted into the pseudo-source root, effectively flattening the ROM structure. If any file clashes occur, the conflicting files are guaranteed to have the exact same contents. Resource packs are archives with the `bactorpack`, `beventpack`, or `pack` raw extension.

#### Downloadable content (DLC)

Downloadable content (DLC), also called add-on content (AoC), is to be extracted into the pseudo-source root. The DLC content root is the romfs root for Switch and the 0010 directory for Wii U.

Any resource that has the same name as a base resource but different contents must be renamed by prepending `.aoc` to the file extension.

For example:

* `path/to/file.ext` -> `path/to/file.aoc.ext`
* `path/to/file.ext.yml` -> `path/to/file.aoc.ext.yml`

### Conversions

#### Decompression

All resources must be stored uncompressed. The .s file extension prefix indicating Yaz0 compression is to be removed.

#### Non-resource-pack SARC archives

SARC archives that are not resource packs must be unpacked into a directory with the same name (including the extension) and location as the original archive.

#### Actor/AnimationInfo resources

For performance reasons, resources in Actor/AnimationInfo must be left untouched, i.e. in their binary form, with the .baniminfo file extension.

#### Message files

msbt files are to be converted to the [msyt](https://github.com/jkcclemens/msyt) format. The resulting files must have the `.msyt` file extension.

#### Map units

`{unit_name}_Static.mubin` and `{unit_name}_Dynamic.mubin` pairs are to be merged into a single *map unit* unit and converted into YAML with the new file name `{unit_name}.muunt.yml`.

Merging consists of:

* Copying the LocationPosX, LocationPosZ and LocationSize top-level properties from the Static map unit (if they exist).
* Adding the IsStatic=true property to each object in the Static map unit.
* Adding the IsStatic=false property to each object in the Dynamic map unit.
* Merging the Objs arrays and sorting the merged array by HashId.
* Merging the Rails arrays and sorting the merged array by HashId.

All remaining resources with the `mubin` file extension must be converted into YAML using the *yaml-byml* specification. They are to be named using the pattern `path/to/filename.mubin` --> `path/to/filename.mubin.yml`.

#### Actor/ActorInfo.product.byml

Useful information is to be extracted from ActorInfo and moved to per-actor metadata files.

For each actor entry in Actor/ActorInfo.product.byml, the tool must determine whether it is a development actor or not. An actor is considered to be a *development actor* if it is not present in the game ROM.

For non-development actors, a new file with all of the following properties (if they exist in the actor entry) is to be created and stored at `Actor/ActorMeta/{actor_name}.yml`:

* aabbMin
* aabbMax
* addColorR
* addColorG
* addColorB
* addColorA
* baseScaleX
* baseScaleY
* baseScaleZ
* boundingForTraverse
* bugMask
* Chemical
* cursorOffsetY
* farModelCulling
* homeArea
* locators
* lookAtOffsetY
* motorcycleEnergy
* rigidBodyCenterY
* sortKey
* terrainTextures
* traverseDist
* variationMatAnim
* variationMatAnimFrame

For development actors, a new file containing the entire actor entry is to be created and stored at `Actor/DevActorMeta/{actor_name}.yml`.

Additionally, in both cases:

* A new property called `instSizeCafe` must be added to the actor metadata. It contains the value of the instSize property for the Nintendo Wii U platform. Its value must be -1 if the size is unknown.
* A new property called `instSizeNx` must be added to the actor metadata. It contains the value of the instSize property for the Nintendo Switch platform. Its value must be -1 if the size is unknown.
* The instSize property is to be removed from the actor metadata.

Finally, the Actor/ActorInfo.product.byml is to be removed from the pseudo-source tree.

#### Event/EventInfo.product.byml

Unlike actors, it is more complicated to determine which events are development events and how to handle them. Moreover, keeping complete metadata allows event editing tools to avoid having to parse other related event files. Thus, the current version of this specification opts for a simple split process for EventInfo.

Event tools should update EventInfo after any event flow edit.

For each event entry in Event/EventInfo.product.byml, a new file containing the entire event entry is to be created and stored at `Event/EventMeta/{event_name}/{entry_point_name}.yml`.

Finally, the Event/EventInfo.product.byml is to be removed from the pseudo-source tree.

#### Quest/QuestProduct.bquestpack

For each quest entry in Quest/QuestProduct.bquestpack, a new file containing the entire quest entry is to be created and stored at `Quest/{quest_name}.quest.yml`.

Finally, the Quest/QuestProduct.bquestpack is to be removed from the pseudo-source tree.

#### GameData resources

savedataformat.sarc and ShopGameDataInfo.byml are to be removed from the pseudo-source as they are automatically generated from the GameData configuration files, map units and shop files.

##### gamedata.sarc

bgdata files must be merged based on their file name. They are to be named using the pattern `filename_%d.bgdata` --> `filename.yml`.

For example, `bool_data_0.bgdata`, `bool_data_1.bgdata`, and `bool_data_2.bgdata` should be merged into a single `bool_data.yml` file. Note that the `revival_bool_data_%d` files are separate even though `bool_data` and `revival_bool_data` both contain boolean GameData flags.

#### AAMP and BYML resources

*Remaining* AAMP and BYML resources in the pseudo-source must be converted into YAML, using the *yaml-aamp* and *yaml-byml* specifications respectively.

They are to be named using the pattern `path/to/filename.ext` --> `path/to/filename.ext.yml`. Any .b file extension prefix is to be removed.

To avoid odd extensions, the following additional extension changes must be made:

* `.yml.yml` -> `.yml`
* `.xml.yml` -> `.yml`
