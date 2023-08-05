# Relationship modeling for entities

The structure will try to take into account other use cases of the information than just the unit counter information.
In the case of the build/scrap helper only, a simple single table solution would be preferable.

Attributes mentioned in this document are the same as those in files **wifunits.drawio** and **wifunits.drawio.png**.

## Notation guide

A relation is presented in following way:

**Name**(_key1_,_key2_,attribute,attribute)

**Name** is the descriptive name for the relation, and _key_ attributes are key values for the relationship.

## Relations

A country can be either a playable major power or other home country for a unit. (The unit is always controlled by a major power, but it's home is not neccessarily a major power country.)

**Country**(_name_, major)

A kit is either the main game or an extension of which the unit and rule options regarding to the unit are part of. It is separated to own table for future proofing.

**Kit**(_name_)

Each numbered option has suboptions which can be chosen to be implemented individually

**Option**(_number_, _name_, kit)

The structure for class, type and type2 attributes is different for land, air (all have class air), and naval units.

**Land\_unit\_type**(_type_, class)

**Air\_unit\_type**(_type_)

**Naval\_unit\_type**(_type2_, type, class)

The attribute year is for most of the units a game year in which the unit becomes available, but some units have special values in it. 
Special values are:

* Empty
* Reserve, unit becomes available when at war with another major power
* City name, unit becomes available after gaining the named city, so called City Based Volunteer
* Ge(+x), unit becomes available when at war with Germany (or USA) + year change after start of the war ranging from 0 to 2

All of these units are unscrappable.

**Regular\_units**(_year_,_unitId_)

**CBV\_units**(_city_,_unitId_)

**Special\_entry\_units**(_unitId_, reserve, ge, ge+1, ge+2, cbv)

Other attribute holds multiple different informations about the unit. In the case of land unit it holds following information:

* White print (better than regular unit in certain situations)
* Artillery unit (regular, anti-tank, anti-air, or FLAK) specific information
  * Artillery (regular, anti-tank, or anti-air) unit movement type:
    * Rail
    * Towed
    * Motorized
    * Self-propelled
  * AT and AA artillery anti-tank capacity type, pink (bonus only in defence) or red (bonus in both attack and defence)
  * AA unit status light (not being able to shoot at high altitude bombers) or heavy
  * Is a regular artillery a rocket artillery
  * Is a FLAK unit Missile or not.
* Is the unit
  * elite
  * commando
  * marine  
  * para
  * mountain
  * motorized
  * airlanding
  * SS
  * Guards
  * Siberian
  * NKVD
  * bicycle

Simplest modeling style would be to have just a **TRUE/FALSE** bit for each of these in a land unit table, but I'll go for a more future proof design.


