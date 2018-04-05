import random
#from Hero import *
from copy import copy
from termcolor import colored,cprint
#     namn, armour, level to use

levelLimits = [30,80,200,1000, 3000]

def createRandomArmour(level):
   if level < 5:
      randCh = random.random()
      if randCh < 0.5:
         rust = TjocktTyg(1)
      elif randCh < 0.85:
         rust = Leather(2)
      else:
         rust = StuddedLeather(4)
      return rust
   else:
      return None  
   
def createRandomShield(level):
   if level < 5:
      randCh = random.random()
      if randCh < 0.5:
         shield = Buckler(1)
      elif randCh < 0.85:
         shield = SmallShield(2)
      else:
         shield = Heater(4)
      return shield
   else:
      return None  


def createRandomWeapon(level):
   if level < 5:
      randCh = random.random()
      if randCh < 0.35:
         weap = SmallClub(1)
      elif randCh < 0.70:
         weap = ShortSword(1)
      elif randCh < 0.90:
         weap = SmallAxe(1)
      else:
         weap = MorningStar(1)
      return weap
   else:
      return None  

class Hero:
   def __init__(self, name, plClass):
      self.level = 0
      self.name = name
      self.position = [0,0]
      self.pclass = plClass
      self.hp = self.heroGetHP(plClass)
      self.hpMax = self.heroGetHP(plClass)
      self.dead = False
      self.mainHand = SmallClub(1)
      self.offHand = None
      self.body = TjocktTyg(1)
      self.xp = 0
      self.poisoned = False
      self.poisonedTurn = 0
      self.poisonDamage = 0 
      self.accuracy = 40
      self.inventory = self.getStartingInventory(plClass)

   def getStartingInventory(self, pclass):
      return [Gold(self.level), HealthPotion(self.level)]

   def getBlock(self):
      if self.offHand:
         shArm = self.offHand.block
      else:
         shArm = 0
      return shArm

   def getArmour(self):
      if self.offHand:
         shArm = self.offHand.armour
      else:
         shArm = 0
      return shArm + self.body.armour
           
   def Attack(self,armour,block,monst):
      print(self.name + " attackerar " + monst.mtype + "!")
      hitRand = random.random()
      if hitRand < (self.accuracy - armour)/100:
         blockRand = random.random()
         if blockRand < block:
            cprint("Attacken blockas!","red")
         else:
            dam = round(self.mainHand.getDamage(self.level))
            cprint(monst.mtype + " tar " + str(dam) + " HP skada!", "cyan")
            monst.hp = monst.hp - dam
            if monst.hp <= 0:
               monst.dead = True
            else:
               cprint(monst.mtype + " har " + str(monst.hp) + " HP kvar.", "cyan")
      else:
         cprint(self.name + " missar!", "red")

   def levelUp(self,monstXp):
      l = self.level
      self.xp = self.xp + monstXp
      xp = self.xp
      newLev = 0
      for lev in levelLimits:
          if xp < lev:
             break
          else:
             newLev = newLev + 1
      dLev = newLev - l
      if dLev > 0:
         cprint("Du har nått level " + str(newLev) + "!", "cyan") 
         self.hpMax = self.hpMax + dLev*5
         self.hp = self.hp + dLev*5
         self.accuracy = self.accuracy + dLev*5
         self.level = newLev

   def applyPoison(self):
      if self.poisoned:
         cprint(self.name + " tar " + str(self.poisonDamage) + " HP skada av gift", "green")
         if self.poisonedTurn == 3:
            self.poisoned = False
            self.poisonedTurn = 0
            self.poisonDamage = 0
         else: 
            self.hp = self.hp - self.poisonDamage
            self.poisonedTurn = self.poisonedTurn + 1
   def heroGetHP(self, pclass):
      if pclass == "Barbar":
         return 25
      elif pclass == "Jägare":
         return 20
      elif pclass == "Magiker":
         return 15
      else:
         return 10

   def pickUp(self,numberStr,room):
      loot = room.getLoot()
      if len(numberStr) == 0:
         cprint("Ange ett nummer!", "red")
         return
      try:
         number = int(numberStr)
      except ValueError:
         cprint("Ange ett nummer!", "red")
         return
      if not number < len(loot):
         cprint("Numret finns inte! Prova igen.","red")
         return
      el = loot[number]
      room.deleteLoot(el)
      added = False
      if type(el) == Gold:
         for i in self.inventory:
            if type(i) == Gold:
               i.count = i.count + el.count
               added = True
         if not added:
            self.inventory.append(el)
      else:
         if len(self.inventory) == 7:
            cprint("Du kan inte bära på fler än 7 saker.","red")
            return
         else:
            self.inventory.append(el)

   def dropItem(self,numberStr,room):
      if len(numberStr) == 0:
         cprint("Ange ett nummer!", "red")
         return
      try:
         number = int(numberStr)
      except ValueError:
         cprint("Ange ett nummer!", "red")
         return
      if not number < len(self.inventory):
         cprint("Numret finns inte! Prova igen.","red")
         return
      el = self.inventory[number]
      room.addLoot(el)
      self.inventory.remove(el)

   def equipWeapon(self,numberStr,room):
      if len(numberStr) == 0:
         cprint("Ange ett nummer!", "red")
         return
      try:
         number = int(numberStr)
      except ValueError:
         cprint("Ange ett nummer!", "red")
         return
      if not number < len(self.inventory):
         cprint("Numret finns inte! Prova igen.","red")
         return
      el = self.inventory[number]
      if not issubclass(type(el),Weapon):   
         cprint("Du har inte valt ett vapen! Prova igen.","red")
      elif self.level < el.levelToUse:   
         cprint("Du har inte nått tillräckligt hög level för att använda vapnet! Prova igen senare.","red")
      else:
         if hasattr(el, "twoHand"):
            if not self.offHand:
               self.inventory.append(self.mainHand)
               self.mainHand = el
               self.inventory.remove(el)
               cprint("Du har bytt vapen","cyan")
            else:
               if len(self.equip) == 7:
                  self.inventory.append(self.mainHand)
                  self.mainHand = el
                  self.inventory.remove(el)
                  room.addLoot(self.offHand)
                  self.offHand = None
                  cprint("Du har bytt vapen, men skölden har släppts på golvet eftersom den inte fick plats","cyan")
               else:
                  self.inventory.append(self.mainHand)
                  self.inventory.append(self.offHand)
                  self.mainHand = el
                  self.inventory.remove(el)
                  self.offHand = None
                  cprint("Du har bytt vapen","cyan")
         else:
            self.inventory.append(self.mainHand)
            self.mainHand = el
            self.inventory.remove(el)
            cprint("Du har bytt vapen","cyan")

   def pr(self):
      nextLev = 0
      goldPr = 0
      for i in self.inventory:
         if type(i) == Gold:
            goldPr = i.count
      if self.offHand:
         shPrint = self.offHand.pr()
      else:
         shPrint = "Ingen sköld"
      for lev in levelLimits:
         if self.xp < lev:
            nextLev = lev
            break

      cprint("=========================","green")
      cprint("Namn: " + self.name + "\nKlass: " + self.pclass + "\nLevel: " + str(self.level) + "\nXP: " + str(self.xp) + "    Nästa level: " + str(nextLev) + "\nHP: " + str(self.hp) + "/" + str(self.hpMax) + "\nVapen: " + self.mainHand.pr() + "\nRustning: " + self.body.pr() + "\nSköld: " + shPrint + "\nGuld: " + str(goldPr),"green")
      if self.poisoned:
         cprint("Du är förgiftad!", "red")
      cprint("=========================","green")

   def showInventory(self):
      ind = 0
      cprint("=========================","green")
      for i in self.inventory:
         cprint(str(ind) + ": " + i.pr(), "green")
         ind = ind + 1
      cprint("=========================","green")

   def equipArmour(self,numberStr,room):
      if len(numberStr) == 0:
         cprint("Ange ett nummer!", "red")
         return
      try:
         number = int(numberStr)
      except ValueError:
         cprint("Ange ett nummer!", "red")
         return
      if not number < len(self.inventory):
         cprint("Numret finns inte! Prova igen.","red")
         return
      el = self.inventory[number]
      print(el)
      if not issubclass(type(el),Armour):   
         cprint("Du har inte valt en rustning! Prova igen.","red")
      elif self.level < el.levelToUse:   
         cprint("Du har inte nått tillräckligt hög level för att använda rustningen! Prova igen senare.","red")
      else:
         self.inventory.append(self.body)
         self.body = el
         self.inventory.remove(el)
         cprint("Du har bytt rustning","cyan")


   def equipShield(self,numberStr,room):
      if len(numberStr) == 0:
         cprint("Ange ett nummer!", "red")
         return
      try:
         number = int(numberStr)
      except ValueError:
         cprint("Ange ett nummer!", "red")
         return
      if not number < len(self.inventory):
         cprint("Numret finns inte! Prova igen.","red")
         return
      el = self.inventory[number]
      if not issubclass(type(el),Shield):   
         cprint("Du har inte valt en sköld! Prova igen.","red")
      elif self.level < el.levelToUse:   
         cprint("Du har inte nått tillräckligt hög level för att använda skölden! Prova igen senare.","red")
      else:
         if self.offHand:
            self.inventory.append(self.offHand)
         self.offHand = el
         self.inventory.remove(el)
         cprint("Du har bytt sköld","cyan")

   def useItem(self,numberStr):
      if len(numberStr) == 0:
         cprint("Ange ett nummer!", "red")

      try:
         number = int(numberStr)
      except ValueError:
         cprint("Ange ett nummer!", "red")
         return
      if not number < len(self.inventory):
         cprint("Numret finns inte! Prova igen.","red")
         return
      el = self.inventory[number]
      if not (type(el) == HealthPotion or type(el) == Antidote):
         cprint("Du kan inte använda den grejen.","red")
         return
      if type(el) == HealthPotion:
         hpAdd = el.hpHeal
         self.hp = min(self.hpMax, self.hp + hpAdd)
         cprint("Du har återfått " + str(hpAdd) + " HP!","cyan")
         self.inventory.remove(el)
      elif type(el) == Antidote:
         self.poisoned = False
         self.poisonedTurn = 0
         self.poisonDamage = 0
         cprint("Du har blivit botad från förgiftningen!","cyan")
         self.inventory.remove(el)
      else:
         cprint("Du kan inte använda den grejen.","red")
      

class Room:
   def __init__(self,hero,dir):
      randLoose = random.random()
      if randLoose < 0.2:
         self.looseTreasure = self.createTreasure(hero.level)
      else: 
         self.looseTreasure = []
      self.exits = self.createExits(dir)
      self.loot = []
      self.hasStairs = False
      self.monsters = self.createMonster(hero.level)
      print("Du står i ett rum.")
      if randLoose < 0.2:
         print("Det ligger en skatt i ett av hörnen.")
      if self.monsters:
         for monster in self.monsters:
            print(monster.mtype + " är här. Den attackerar dig!")
    
   def printExits(self):
      print("Det finns utgångar till " + str(self.exits) + ".") 

   def printMonsters(self):
      cprint("===========================","green")
      for monst in self.monsters:
         printString = "Namn: " + monst.mtype + "\nHP: " + str(monst.hp) + "\nRustning: " + str(monst.armour) +  "\n" 
         if monst.dead:
            cprint(printString,"red")
         else:
            cprint(printString,"green")
      cprint("===========================","green")
      
   def createExits(self,dir):
      possExits = ["n", "e", "s", "w"]
      exits = []
      exPoss = []
      nExits  = random.randint(1,3)
      while len(exits) < nExits:
         randExt = random.randint(0,nExits)
         dirUt = possExits[randExt]
         if not dirUt in exits and not dirUt == dir:
            exits.append(dirUt)
      return exits

   def showMonsters(self):
      if len(self.monsters) == 1:
         return self.monsters[0]
      else:
         chosen = false
         while not chosen:
            print("Dessa monster finns i rummet. Vilken vill du attackera?")
            for i in range(0,len(self.monsters)):
               print(str(i) + ": " + self.monsters[i].mtype)
            inpNumb = input("Skriv numret här: ")
            if inpNumb <= len(self.monsters):
               return self.monsters[inpNumb]
            else:
               print("Fel nummer. Försök igen.")
       

   def removeMonster(self, monster):
      self.monsters = monsters.remove(monster)

   def getLoot(self):
      allThings = copy(self.loot)
      if self.looseTreasure:
         allThings.insert(0,self.looseTreasure)
      return allThings

   def addLoot(self,lootElement):
      self.loot.append(lootElement)

   def deleteLoot(self,lootElement):
      if self.looseTreasure == lootElement:
         self.looseTreasure = None
      else:
         self.loot.remove(lootElement)

   def showLoot(self):
      allThings = self.loot
      loose = self.looseTreasure
      if len(allThings) == 0 and not loose:
         print("Det finns inget här.")
      else:
         print("Detta ligger på golvet:")
         startRange = 0
         cprint("===================","green")
         if loose:
            cprint("0: " + loose.pr(), "green")
            startRange = 1
            
         for i in range(0,len(allThings)):
            el = allThings[i]
            cprint(str(i+startRange) + ": " + el.pr(),"green")
         cprint("===================","green")

   def createTreasure(self,level):
      if level < 5:
         return self.createMiscTreasure(level)
      elif level < 10:
         trRand = random.randint(0,1)
         if trRand == 0:
           return self.createMiscTreasure(level)
         else:
           return self.createOther(level)
      else:
           return self.createOther(level)

   def createMiscTreasure(self,level):
      randChoice = random.random()
      if randChoice < 0.45:
         return Gold(level)
      elif randChoice < 0.9:
         return HealthPotion(level)
      else:
         return Antidote(level)

   def createOther(self,level):
      randChoice = random.random()
      if randChoice < 0.45:
         return self.createWeapon(level)
      elif randChoice < 0.8:
         return self.createArmour(level)
      else:
         return self.createShield(level)

   def createArmour(self,level):
      return createRandomArmour(level)

   def createWeapon(self,level):
      return createRandomWeapon(level)

   def createShield(self,level):
      return createRandomShield(level)

   def createMonster(self,level):
      randMon = random.random()
      if randMon < 0.15:
         return None
      else:
         return [Monster(level)]
 

class TreasureObject:
   def __init__(self, level, objType, levelToUse):
      self.level = level
      self.levelToUse = levelToUse
      self.objType = objType
      self.properties = self.getProperties(level, objType)
      self.name = self.getName(objType, self.properties)


   def getName(self, typ, props):
      return typ
      
   def randProp(self, level, typ):
      return ["Gift",1,["extra_damage", 4]]

   def getProperties(self, level, objType):
      utSk = []
      if objType == "Guld":
         return []
      elif objType == "Motgift":
         return []
      elif objType == "Helande dryck":
         return []
      else: 
         if level < 5:
            nProperties = 1
         elif level < 10:
            nProperties = 2
         else:
            nProperties = 3

      for i in range(nProperties):
         utSk.append(self.randProp(level, objType))

      return utSk

   def displayTreasure(self):
      print("Treasure of type " + str(self.objType) + " with properties " + str(self.properties) + " created")

class MiscTreasureObject(TreasureObject):
   def __init__(self, level, type, lToUse):
      TreasureObject.__init__(self,level, type, lToUse)

class Gold(TreasureObject):
   def __init__(self, level):
      TreasureObject.__init__(self,level, "Guld", 0)
      self.count = self.getGoldAmount(level) 
   def getGoldAmount(self,level):
      randAm = random.uniform(0.5,1.5)
      return  round((level + 1)*randAm*100) 
   def pr(self):
      return self.name + ": " + str(self.count) + " mynt"    
  
class EasterEgg(TreasureObject):
   def __init__(self, level):
      TreasureObject.__init__(self,level, "Ett Påskägg!", 0)
   def pr(self):
      return self.name

class GreenDiamond(TreasureObject):
   def __init__(self, level):
      TreasureObject.__init__(self,level, "Den gröna diamanten", 0)
   def pr(self):
      return self.name

class HealthPotion(TreasureObject):
   def __init__(self, level):
      TreasureObject.__init__(self,level, "Helande dryck", 0)
      self.hpHeal = self.getHpHeal(level) 
   def getHpHeal(self,level):
      randAm = random.uniform(0.5,1.5)
      return  round((level + 1)*3*randAm + 10) 
   def pr(self):
      return self.name + ", helar " + str(self.hpHeal) + " HP"    

class Antidote(TreasureObject):
   def __init__(self, level):
      TreasureObject.__init__(self,level, "Motgift", 0)
   def pr(self):
      return self.name + ", botar gift."

class Weapon(TreasureObject):
   def __init__(self, level, type, lToUse):
      TreasureObject.__init__(self,level, type, lToUse)
   def getDamage(self, level, type):
      return 5;
   def pr(self):
      return self.name  
   
class Armour(TreasureObject):
   def __init__(self, level, typ, armour, lToUse):
      TreasureObject.__init__(self,level, typ, lToUse)
      self.armour = armour
   def randProp(self, level, typ):
      if level < 5:
         props = [["Stensköld",0.5,["extra_armour", 4, "skydd"]], ["Totalblock", 0.1, ["extra_armour",20, "skydd"]]]
         randVal = random.randint(0,1)
      return props[randVal]
   def pr(self):
      return self.name + ": skyddar " + str(self.armour)

class TjocktTyg(Armour):
   def __init__(self, level):
      Armour.__init__(self, level, "Tjockt tyg", 3,  0)

class Leather(Armour):
   def __init__(self, level):
      Armour.__init__(self, level, "Läder", 5, 1)

class StuddedLeather(Armour):
   def __init__(self, level):
      Armour.__init__(self, level, "Nitläder", 8, 4)
         
         
class Shield(TreasureObject):
   def __init__(self, level, typ, armour, block, lToUse):
      TreasureObject.__init__(self,level, typ, lToUse)
      self.block = block
      self.armour = armour
   def pr(self):
      return self.name + ": skyddar " + str(self.armour) + " och blockar " + str(self.block*100) + " % av gångerna"
  
class Buckler(Shield):
   def __init__(self, level):
      Shield.__init__(self, level, "Bucklare",  2, 0.3, 0)

class SmallShield(Shield):
   def __init__(self, level):
      Shield.__init__(self, level, "Liten sköld", 3, 0.35 , 3)

class Heater(Shield):
   def __init__(self, level):
      Shield.__init__(self, level, "Rundsköld", 3, 0.4, 5)

class SharpWeapon(Weapon):
   def __init__(self, level, type, lToUse):
      Weapon.__init__(self,level,type,lToUse)
      self.sharp = True
      self.blunt = False
   def randProp(self, level, typ):
      if level < 5:
         props = [["Frost",0.3,["extra_damage", 3, "köld"]], ["Eld",0.5,["extra_damage", 2, "eld"]], ["Extra vasst",0.6,["extra_damage", 3, "skada"]], ["Dråpslag",0.2,["extra_damage", 10, "skada"]]]
         randVal = random.randint(0,4)
      return props[randVal-1]
   def getDamage(self,level):
      return 5

class BluntWeapon(Weapon):
   def __init__(self, level, type, lToUse):
      Weapon.__init__(self,level,type, lToUse)
      self.blunt = True
      self.sharp = False
   def getDamage(self,level):
      return 5

class SmallAxe(SharpWeapon):
   def __init__(self, level):
      SharpWeapon.__init__(self,level,"Liten Yxa", 3)
   def getDamage(self,level):
      dLev = min(level,5)
      randDam = random.uniform(0.7,1.3)
      dam = 3*(dLev+1)*randDam + 3 
      return dam

class ShortSword(SharpWeapon):
   def __init__(self, level):
      SharpWeapon.__init__(self,level,"Kortsvärd", 1)
   def getDamage(self,level):
      dLev = min(level,5)
      randDam = random.uniform(0.8,1.2)
      dam = 3*(dLev+1)*randDam + 1 
      return dam

class TwoHandSword(SharpWeapon):
   def __init__(self, level):
      SharpWeapon.__init__(self,level,"Tvåhandssvärd", 5)
      self.twoHand = True
   def getDamage(self,level):
      dLev = min(level,5)
      randDam = random.uniform(0.8,1.2)
      dam = 6*(dlev+1)*randDam + 2 
      return dam

class Maul(BluntWeapon):
   def __init__(self, level):
      BluntWeapon.__init__(self,level,"Slägga", 7)
      self.twoHand = True
   def getDamage(self,level):
      dLev = min(level,5)
      randDam = random.uniform(0.4,1.6)
      dam = 8*(dlev+1)*randDam + 4 
      return dam

class SmallClub(BluntWeapon):
   def __init__(self, level):
      BluntWeapon.__init__(self,level,"Liten klubba", 0)
   def getDamage(self,level):
      dLev = min(level,5)
      randDam = random.uniform(0.6,1.4)
      dam = 4*(dLev+1)*randDam + 1 
      return dam

class MorningStar(BluntWeapon):
   def __init__(self, level):
      BluntWeapon.__init__(self,level,"Morgonstjärna", 5)
   def getDamage(self,level):
      dLev = min(level,5)
      randDam = random.uniform(0.5,1.5)
      dam = 3.5*(dLev+1)*randDam + 5 
      return dam



class Monster:
   def __init__(self, level):
      self.level = level
      self.dead = False
      self.looted = False
      self.startRoaming = False
      self.block = 0
      self.mtype = self.getMonsterType(level)
      self.armour = self.getMonsterArmour(level)
      self.weaknesses = self.getWeaknesses(level, self.mtype)
      self.abilities = self.getMonsterAbilities(level, self.mtype)
      self.hp = self.getHP(level, self.mtype)
      self.damage = self.getMonsterDamage(level, self.mtype)
      self.accuracy = self.getAccuracy(level,self.mtype)
      self.xp = self.getXP(level,self.abilities)

   def getXP(self, level, abilities):
      baseXP = level*level + 10 + random.randint(0,10)*level
      extXP = len(abilities)* level
      return baseXP+extXP

   def getMonsterArmour(self,level): 
      typ = self.mtype
      randD = random.uniform(0.8,1.2)
      if typ == "Råttan":
         dmg = randD*(level+1)*2 
      elif typ == "Huggormen": 
         dmg = randD*(level+1)*2 + 3 
      elif typ == "Mördarsnigeln": 
         dmg = randD*(level+1)*3 + 10 
      elif typ == "Påskharen": 
         dmg = randD*(level+1)*1 
      elif typ == "Jättebävern": 
         dmg = randD*(level+1)*2  + 2 
      elif typ == "Jätteeldmyran": 
         dmg = randD*(level+1)*1  + 2 
      elif typ == "Frostörn": 
         dmg = randD*(level+1)*2  + 5 
      else:
         dmg = 4
      return round(dmg)


   def getMonsterDamage(self,level,typ): 
      randD = random.uniform(0.8,1.2)
      if typ == "Råttan":
         dmg = randD*(level+1)*2 + 1
      elif typ == "Huggormen": 
         dmg = randD*(level+1)*2 
      elif typ == "Mördarsnigeln": 
         dmg = randD*(level+1)*1 + 1 
      elif typ == "Påskharen": 
         dmg = randD*(level+1)*1 
      elif typ == "Jättebävern": 
         dmg = randD*(level+1)*1.5 + 3 
      elif typ == "Jätteeldmyran": 
         dmg = randD*(level+1)*1.1 + 1 
      elif typ == "Frostörn": 
         dmg = randD*(level+1)*2.5 + 1 
      else:
         dmg = 4
      return round(dmg)

   def getHP(self,level,typ):
      randD = random.uniform(0.8,1.2)
      if typ == "Råttan":
         hp = randD*(level+1)*6 + 10
      elif typ == "Huggormen": 
         hp = randD*(level+1)*4 + 10 
      elif typ == "Mördarsnigeln": 
         hp = randD*(level+1)*10  + 20
      elif typ == "Påskharen": 
         hp = randD*(level+1)*20 
      elif typ == "Jättebävern": 
         hp = randD*(level+1)*7.5 
      elif typ == "Jätteeldmyran": 
         hp = randD*(level+1)*5
      elif typ == "Frostörn": 
         hp = randD*(level+1)*6 + 5
      else:
         hp = 4
      return round(hp)

   def getAccuracy(self,level,typ):
      randD = random.uniform(0.8,1.2)
      if typ == "Råttan":
         hp = randD*(level+1)*5 + 20
      elif typ == "Huggormen": 
         hp = randD*(level+1)*6 + 30
      elif typ == "Mördarsnigeln": 
         hp = randD*(level+1)*1 + 20
      elif typ == "Påskharen": 
         hp = randD*(level+1)*1 + 20
      elif typ == "Jättebävern": 
         hp = randD*(level+1)*5 + 20
      elif typ == "Jätteeldmyran": 
         hp = randD*(level+1)*5 + 20
      elif typ == "Jätteeldmyran": 
         hp = randD*(level+1)*4 + 20
      else:
         hp = 4
      return round(hp)


   def getWeaknesses(self,level, typ):
      weaknesses = ["eld", "köld","trubb","skär"]
      weakRet = []
      if level < 5:
         nWeak = 2;
      elif level < 10:
         nWeak = random.randint(1,2)
      elif level < 15:
         nWeak = 1
      else:
         return []
      done = False
      while not done:
         if len(weakRet) == nWeak:
            return weakRet
         else:
            weakrand = random.randint(0,len(weaknesses)-1)
            weak = weaknesses[weakrand]
            if not weak in weakRet:
               weakRet.append(weak)

   def createLoot(self,level):
      cprint("Monstret dog och tappade något på golvet!", "cyan")
      retLoot = []
      if self.mtype == "Påskharen":
         return [EasterEgg(1)]
      if level < 10:
         randMisc = random.random()
         if randMisc < 0.6:
            retLoot.append(Gold(level))
         elif randMisc < 0.85:
            retLoot.append(HealthPotion(level))
         else:
            retLoot.append(Antidote(level))
         nrLootRand = random.random()
         if nrLootRand < 0.5:
            nrLoot = 0
            return retLoot
         elif nrLootRand < 0.9:
            nrLoot = 1
         else:
            nrLoot = 2
         for j in range (0,nrLoot):
            randType = random.random()
            if randType < 0.6:
               retLoot.append(createRandomWeapon(level))
            elif randType < 0.8:
               retLoot.append(createRandomArmour(level))
            elif randType < 0.95:
               retLoot.append(createRandomShield(level))
            else:
               if self.level > 5:
                  retLoot.append(GreenDiamond(5))
               else:
                  retLoot.append(createRandomShield(level))
                 
         return retLoot
      else:
         return []

   def getBlock(self):
      return 0

   def getArmour(self):
      return 0

   def getMonsterType(self,level):
      if level < 3:
         rand = random.randint(0,2)
         return ["Råttan", "Huggormen", "Mördarsnigeln"][rand]
      elif level < 6:
         rand = random.randint(0,2)
         return ["Jättebävern", "Jätteeldmyran", "Frostörnen"][rand]
      elif level < 10:
         rand = random.randint(0,2)
         return ["Gnomen", "Harpyan", "Svartalfen"][rand]
      else:
         return "Jätten"

   def monsterAttack(self,armour,block,hero):
      print(self.mtype + " attackerar " + hero.name + "!")
      typeOfAttack = random.random()
      extDam = 0
      for ability in self.abilities:
         if typeOfAttack < ability[1]:
            abExtra = ability[2]
            cprint(self.mtype + " använder " + ability[0] + "!","red")
            if abExtra[0] == "extraDamage":
               extDam = abExtra[1]
            elif abExtra[0] == "poison":
               hero.poisoned = True
               hero.poisonedTurn = 1
               hero.poisonDamage = abExtra[1]
               cprint("Du har blivit förgiftad!","green")
      hitRand = random.random()
      if hitRand < (self.accuracy - armour)/100:
         blockRand = random.random()
         if blockRand < block:
            cprint("Attacken blockas!","cyan")
         else:
            randDam = random.uniform(0.8,1.2)
            fullDam = round(self.damage*randDam + extDam)
             
            cprint(hero.name + " tar " + str(fullDam) + " HP skada!", "red")
            hero.hp = hero.hp - fullDam
            if hero.hp <= 0:
               cprint(hero.name + " har dött!", "red")
               hero.dead = True
            else:
               cprint(hero.name + " har " + str(hero.hp) + "HP kvar.","yellow")
               
      else:
         cprint(self.mtype + " missar!","cyan")

   def getMonsterAbilities(self,level,typ):
      if typ == "Råttan":
         return [["Huggbett", 0.25, ["extraDamage", 5 + level/2]]]
      elif typ == "Huggormen": 
          return [["Gift", 0.40, ["poison", 1 + level]]]
      elif typ == "Mördarsnigeln": 
          return [["Slembett", 0.10, ["extraDamage", 10 + level]]]
      elif typ == "Jättebävern": 
          return [["Svansdunk", 0.25, ["extraDamage", 6 + level + 2]]]
      elif typ == "Jätteeldmyran": 
          return [["Eldspott", 0.3, ["eld", 7 + level/2]], ["Giftbett", 0.3, ["poison", 3]]]
      elif typ == "Frostörn": 
          return [["Frysande klor", 0.4, ["köld", level*2]]]
      else:
         return []

   def displayMonster(self):
      print("Monster of type " + str(self.mtype) + " with abilities " + str(self.abilities) + " with " + str(self.hp) + " HPs and " + str(self.accuracy) + " accuracy")


cprint("======================================================","cyan")
print("Välkommen! Kan du hitta den gröna diamanten nere i grottorna?")
heroName = input("Ge oss ditt namn, hjälte:")

hero = Hero(heroName,"Barbar")

firstTime = True
nextRoom = False
missionObjective = False
while not hero.dead:
   print("\n")
   dir = "n"
   exiting = False
   exitingInput = False
   hero.applyPoison()
   if firstTime:
      room = Room(hero,dir)
      monsters = room.monsters
   if monsters: 
      if not hero.dead:
         monstToAttack = room.showMonsters()
         if not monstToAttack.dead:
            hero.Attack(monstToAttack.armour,monstToAttack.block, monstToAttack)
      for monster in monsters:
         if not monster.dead:
            monster.monsterAttack(hero.getArmour(),hero.getBlock(),hero)
      else: 
         exiting = True
   
   if monsters: 
      for monster in monsters:
         if monster.dead and not monster.looted:
            hero.levelUp(monster.xp)
            room.loot = monster.createLoot(hero.level)
            monster.looted = True
#            room.removeMonster(monster)
   if firstTime:
      nextRoom = False
   firstTime = False
   while not exitingInput:
      if missionObjective == True:
         cprint("Grattis " + hero.name + "! Du har vunnit spelet!","green")
         exit(0)
      if hero.dead == True:
         cprint("Du har tyvärr dött! Prova gärna igen.","red")
         totGold = 0
         for i in hero.inventory:
            if type(i) == Gold:
               totGold = i.count
         cprint("Du samlade ihop totalt " + str(totGold) + " guld. Bra jobbat!","green")
         
         exit(0)
      room.printExits()
      inp = input("\nSkriv w/e/n/s för att gå i motsvarande riktning.\nc för att fortsätta strida.\nh för att se hjältens egenskaper\ni för att se vad hjälten bär.\na för att använda ett föremål\nf för att se vad som finns på golvet att plocka upp.\nd för att släppa ett föremål.\np för att ta upp ett föremål.\nv för att välja ett vapen.\nr för att välja rustning.\nk för att välja sköld.\nm för att se monstrens egenskaper.")
      if inp == "w" or inp == "e" or inp == "s" or inp == "n":
         if not inp in room.exits:
            print("Det går inte att gå ditåt")
         else:
            firstTime = True
            exitingInput = True
            nextRoom = True
      elif inp == "i": 
         hero.showInventory()
      elif inp == "h": 
         hero.pr()
      elif inp == "f": 
         room.showLoot()
      elif inp == "m": 
         room.printMonsters()
      elif inp == "d":
         inpNr = input("Ge numret på föremålet.")
         hero.dropItem(inpNr, room)
      elif inp == "p":
         inpNr = input("Ge numret på föremålet.")
         hero.pickUp(inpNr, room)
      elif inp == "v":
         inpNr = input("Ge numret på föremålet.")
         hero.equipWeapon(inpNr, room)
      elif inp == "r":
         inpNr = input("Ge numret på föremålet.")
         hero.equipArmour(inpNr, room)
      elif inp == "a":
         inpNr = input("Ge numret på föremålet.")
         hero.useItem(inpNr)
      elif inp == "k":
         inpNr = input("Ge numret på föremålet.")
         hero.equipShield(inpNr,room)
      elif inp == "c":
         exitingInput = True  
      else:
         print("Det finns inget sådant kommando")
         
         
    







