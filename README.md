## ZeldaBuilder

### TODO

* PERF: switch to rapidyaml?
* figure out which data is present in ActorInfo

  note: extracted ActorParam keys appear to follow the naming convention: table name (camelCase) + parameter name

#### Unbuilder
* generate files from scratch:
  * dev events
  * EventInfo
  * QuestProduct -> one file per quest. .quest.yml
  * GameData -> split by flag type, support extra include directories, get rid of revival flags (autogenerate them)

#### Builder
* figure this out.

* ActorInfo drops: Add "Amiibo: 1" if the actor has amiibo drop tables.
* dependency system to put resources and their dependencies in archives easily
    * implement this with "resource groups"?
* hardcoded list of resources to put in Bootup/TitleBG (+ resident actors / events)
* have an index of source files to track changes and rebuild only what has changed
* have a command to manually mark all files as up-to-date (to avoid having to build unmodified files)

## License

This software is licensed under the terms of the GNU General Public License, version 2 or later.
