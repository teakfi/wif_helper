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

**Option**(_id_, number, name, description, kit)

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

CBV information is saved here.

**CBV\_units**(_city_,_unitId_)

Special entry information with booleans, maximum one active, if none, then the unit has "empty" as year attribute.

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

Simplest modeling style would be to have just a **TRUE/FALSE** bit for each of these in a land unit table and I'll go with it for now.

For air units other incorporates following information:

* High altitude capable (high)
* Air transport capable (atr)
* Paradrop capable (para)
* Land-lease information
* Night fighter (nf)
* Unarmed
* Jet
* Tank buster (tb)
* Extended range available (ext)
* Sub-hunter (sh)
* low altitude (low)
* 2 engine fighter (2e)
* not paradrop capable (np)
* large air transport (xatr)
* flying boat (fb)
* white skull (ws)
* black skull (bs)
  
Here all else expect land-lease information are simple **TRUE/FALSE** statements.

Land-lease units cannot be build by the user country, they must be received from the original owner of the unit which is then made unavailable. For a land-lease unit there is an original unit available for be given as a LL by the original owner, but there may be multiple possible recipients for the same unit. An example of this is an USA build aircraft which is available as an LL aircraft for both France and Commonwealth.

**LandLease**(_originalUnitId_,_loanUnitId_)

Carriers have maximum size of aircraft which can be based on the carrier. Carrier aircrafts (CVP) have a corresponding size attribute, which depends of the game year. The size can decrease by one up to twice to minimum size of 1 during specific years.

**CVPSize**(_unitId_, startingSize)
**CVPSizeDropYear**(_unitId_. dropYear)

The ship2 attribute in the data holds various information. 

* for a convoy units ship1 and ship2 are number of convoy points represented by the counter
* for a regular game battleship it has the name of second ship the counter represents
* for an ASW unit it has the name of the unit as ship1 has the number of convoy points
* for a frogman unit it has the seabox value
* some units have information if the unit has a replacement (update which needs to be build)
* some units have information if the unit is a replacement for previous unit with same name
* Land Lease information
* Transport being capable to transport only INF-class units
* Submarine having a schnorkel, Walther, missiles, and/or being a milchcow
* Transport being a service squadron (ssq) and the size of port stacking bonus

**Replacements**(_replacedId_,_replacementId_)

For representing convoy capability I decided to give each naval unit convoy cap 1 and 2 (cc1,cc2) representing convoy unit capacity and asw unit capacity. This allows also representation of future special counters with convoy capability.
Unit names will be 
  
**Land\_unit**(_unitId_, typeId, powerCountry, homeCountry, name, optionId, buildTime, buildCost, strenght, movementspeed, reorgvalue, divSized, WP, railmov, towed, motorized, SP, pink, red,  heavyAA, rocket, missileFLAK, elite, commando, marine, para, mountain, airlanding, SS, guards, Siberian, NKVD, bicycle)

**Air\_unit**(_unitId_, typeId, powerCountry, homeCountry, unit, name, optionId, buildTime, buildCost, ATA, ATS, TAC, RNG, STR, high, atr, para, nf, unarmed, jet, tb, ext, sh, low, 2e, np, xatr, fb, ws, bs, ll_able, ll_unit)

**Naval\_unit**(_unitId_, typeId, powerCountry, homeCountry, shipname, optionId, buildTime, buildCost, buildCost2, cc1, cc2, replaceable, replacement, ll_able, ll_unit, seabox, inf_transport_only, schnorkel, walther, missile, milchcow, ssqValue, att, def, rng, mov, cv, sb, aa, sunkDate, used)
