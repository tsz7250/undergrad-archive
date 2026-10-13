.data
str0: .string "s1111452\n"
last1: .string "Please enter the strokes of the first character of the last name (If you only have one characters of your last name, input 1) =  "
last2: .string "Please enter the strokes of the second character of the last name = "
first1: .string "Please enter the strokes of the first character of the first name = "
first2: .string "Please enter the strokes of the second character of the first name (If you only have one characters of your first name, input 1) = "

equalSign: .string " = "

sky: .string "Sky"
People: .string "People"
Land: .string "Land"
Outside: .string "Outside"
total: .string "Total"

wood: .string " Wood\n"   
fire: .string " Fire\n"
Earth: .string " Earth\n"
Metal: .string " Metal\n"
Water: .string " Water\n"

SEP: .string "Sky Equal People\n"
SEL: .string "Sky Equal Land\n"
SEO: .string "Sky Equal Outside\n"
SET: .string "Sky Equal Total\n"

SGP: .string "Sky Generate People\n"
SGL: .string "Sky Generate Land\n"
SGO: .string "Sky Generate Outside\n"
SGT: .string "Sky Generate Total\n"

SRP: .string "Sky Restraint People\n"
SRL: .string "Sky Restraint Land\n"
SRO: .string "Sky Restraint Outside\n"
SRT: .string "Sky Restraint Total\n"

PEL: .string "People Equal Land\n"
PEO: .string "People Equal Outside\n"
PET: .string "People Equal Total\n"

PGS: .string "People Generate Sky\n"
PGL: .string "People Generate Land\n"
PGO: .string "People Generate Outside\n"
PGT: .string "People Generate Total\n"

PRS: .string "People Restraint Sky\n"
PRL: .string "People Restraint Land\n"
PRO: .string "People Restraint Outside\n"
PRT: .string "People Restraint Total\n"

LEO: .string "Land Equal Outside\n"
LET: .string "Land Equal Total\n"

LGS: .string "Land Generate Sky\n"
LGP: .string "Land Generate People\n"
LGO: .string "Land Generate Outside\n"
LGT: .string "Land Generate Total\n"

LRS: .string "Land Restraint Sky\n"
LRP: .string "Land Restraint People\n"
LRO: .string "Land Restraint Outside\n"
LRT: .string "Land Restraint Total\n"

OET: .string "Outside Equal Total\n"

OGS: .string "Outside Generate Sky\n"
OGP: .string "Outside Generate People\n"
OGL: .string "Outside Generate Land\n"
OGT: .string "Outside Generate Total\n"

ORS: .string "Outside Restraint Sky\n"
ORP: .string "Outside Restraint People\n"
ORL: .string "Outside Restraint Land\n"
ORT: .string "Outside Restraint Total\n"

TGS: .string "Total Generate Sky\n"
TGP: .string "Total Generate People\n"
TGL: .string "Total Generate Land\n"
TGO: .string "Total Generate Outside\n"

TRS: .string "Total Restraint Sky\n"
TRP: .string "Total Restraint People\n"
TRL: .string "Total Restraint Land\n"
TRO: .string "Total Restraint Outside\n"
.text
main:
	jal printSID

    jal printlast1
    jal Inputlast1

    jal printlast2
    jal Inputlast2

    jal printfirst1
    jal Inputfirst1

    jal printfirst2
    jal Inputfirst2

    jal printNewLine

    jal CalSky
    jal printSky
    jal printEqualSign
    jal printResult
    jal SetSkyElement
    jal PrintElement

    jal CalPeople
    jal printPeople
    jal printEqualSign
    jal printResult
    jal SetPeopleElement
    jal PrintElement

    jal CalLand
    jal printLand
    jal printEqualSign
    jal printResult
    jal SetLandElement
    jal PrintElement

    jal CalOutside
    jal printOutside
    jal printEqualSign
    jal printResult
    jal SetOutsideElement
    jal PrintElement

    jal CalTotal
    jal printTotal
    jal printEqualSign
    jal printResult
    jal SetTotalElement
    jal PrintElement

    jal printNewLine

    jal CheckSEP
    jal CheckSEL
    jal CheckSEO
    jal CheckSET
    jal CheckSGP
    jal CheckSGL
    jal CheckSGO
    jal CheckSGT
    jal CheckSRP
    jal CheckSRL
    jal CheckSRO
    jal CheckSRT

    jal CheckPEL
    jal CheckPEO
    jal CheckPET
    jal CheckPGS
    jal CheckPGL
    jal CheckPGO
    jal CheckPGT
    jal CheckPRS
    jal CheckPRL
    jal CheckPRO
    jal CheckPRT

    jal CheckLEO
    jal CheckLET
    jal CheckLGS
    jal CheckLGP
    jal CheckLGO
    jal CheckLGT
    jal CheckLRS
    jal CheckLRP
    jal CheckLRO
    jal CheckLRT

    jal CheckOET
    jal CheckOGS
    jal CheckOGP
    jal CheckOGL
    jal CheckOGT
    jal CheckORS
    jal CheckORP
    jal CheckORL
    jal CheckORT

    jal CheckTGS
    jal CheckTGP
    jal CheckTGL
    jal CheckTGO
    jal CheckTRS
    jal CheckTRP
    jal CheckTRL
    jal CheckTRO

    j end

printSID:
	la a0, str0			
	li a7, 4			
 	ecall
 	ret

printlast1:
    la a0, last1		
    li a7, 4			
 	ecall
 	ret
printlast2:
    la a0, last2		
    li a7, 4			
    ecall
    ret
printfirst1:
    la a0, first1		
    li a7, 4			
    ecall
    ret
printfirst2:
    la a0, first2		
    li a7, 4			
    ecall
    ret
printSky:
    la a0, sky			
    li a7, 4			
    ecall
    ret
printPeople:
    la a0, People		
    li a7, 4			
    ecall
    ret
printLand:
    la a0, Land			
    li a7, 4			
    ecall
    ret
printOutside:
    la a0, Outside		
    li a7, 4			
    ecall
    ret
printTotal:
    la a0, total		
    li a7, 4			
    ecall
    ret
printWood:
    la a0, wood
    li a7, 4
    ecall
    ret
printFire:
    la a0, fire
    li a7, 4
    ecall
    ret
printEarth:
    la a0, Earth
    li a7, 4
    ecall
    ret
printMetal:
    la a0, Metal
    li a7, 4
    ecall
    ret
printWater:
    la a0, Water
    li a7, 4
    ecall
    ret

Inputlast1:
    li s4, 12
    li a7,5
    ecall
    mv s1, a0
    ret
Inputlast2:
    li s4, 12
    li a7,5
    ecall
    mv s2, a0
    ret
Inputfirst1:
    li s4, 12
    li a7,5
    ecall
    mv s3, a0
    ret
Inputfirst2:
    li s4, 12
    li a7,5
    ecall
    mv s4, a0
    ret

CalSky:
    li t0,0
    add t0, s1, s2
    mv s0, t0
    ret
CalPeople:
    li t0,0
    add t0, s2, s3
    mv s0, t0
    ret
CalLand:
    li t0,0
    add t0, s3, s4
    mv s0, t0
    ret
CalOutside:
    li t0,0
    add t0, s1, s4
    mv s0, t0
    ret
CalTotal:
    li t0, 0
    li t1, 1
    add t0, s2, s3
    bne s1, t1, adds1
    bne s4, t1, adds4
moveResult:
    mv s0, t0
    ret
adds1:
    add t0, t0, s1
adds4:
    add t0, t0, s4
    j moveResult

SetSkyElement:
    #s0 = s0 mod 10
    li t0, 10
    rem s0, s0, t0

    li t0, 1
    beq s0, t0, SkyisWood
    li t0, 2
    beq s0, t0, SkyisWood

    li t0, 3
    beq s0, t0, SkyisFire
    li t0, 4
    beq s0, t0, SkyisFire

    li t0, 5
    beq s0, t0, SkyisEarth
    li t0, 6
    beq s0, t0, SkyisEarth

    li t0, 7
    beq s0, t0, SkyisMetal
    li t0, 8
    beq s0, t0, SkyisMetal

    li t0, 9
    beq s0, t0, SkyisWater
    li t0, 0
    beq s0, t0, SkyisWater
    ret

SetPeopleElement:
    #s0 = s0 mod 10
    li t0, 10
    rem s0, s0, t0

    li t0, 1
    beq s0, t0, PeopleisWood
    li t0, 2
    beq s0, t0, PeopleisWood

    li t0, 3
    beq s0, t0, PeopleisFire
    li t0, 4
    beq s0, t0, PeopleisFire

    li t0, 5
    beq s0, t0, PeopleisEarth
    li t0, 6
    beq s0, t0, PeopleisEarth

    li t0, 7
    beq s0, t0, PeopleisMetal
    li t0, 8
    beq s0, t0, PeopleisMetal

    li t0, 9
    beq s0, t0, PeopleisWater
    li t0, 0
    beq s0, t0, PeopleisWater
    ret

SetLandElement:
    #s0 = s0 mod 10
    li t0, 10
    rem s0, s0, t0

    li t0, 1
    beq s0, t0, LandisWood
    li t0, 2
    beq s0, t0, LandisWood

    li t0, 3
    beq s0, t0, LandisFire
    li t0, 4
    beq s0, t0, LandisFire

    li t0, 5
    beq s0, t0, LandisEarth
    li t0, 6
    beq s0, t0, LandisEarth

    li t0, 7
    beq s0, t0, LandisMetal
    li t0, 8
    beq s0, t0, LandisMetal

    li t0, 9
    beq s0, t0, LandisWater
    li t0, 0
    beq s0, t0, LandisWater
    ret

SetOutsideElement:
    #s0 = s0 mod 10
    li t0, 10
    rem s0, s0, t0

    li t0, 1
    beq s0, t0, OutsideisWood
    li t0, 2
    beq s0, t0, OutsideisWood

    li t0, 3
    beq s0, t0, OutsideisFire
    li t0, 4
    beq s0, t0, OutsideisFire

    li t0, 5
    beq s0, t0, OutsideisEarth
    li t0, 6
    beq s0, t0, OutsideisEarth

    li t0, 7
    beq s0, t0, OutsideisMetal
    li t0, 8
    beq s0, t0, OutsideisMetal

    li t0, 9
    beq s0, t0, OutsideisWater
    li t0, 0
    beq s0, t0, OutsideisWater
    ret

SetTotalElement:
    #s0 = s0 mod 10
    li t0, 10
    rem s0, s0, t0

    li t0, 1
    beq s0, t0, TotalisWood
    li t0, 2
    beq s0, t0, TotalisWood

    li t0, 3
    beq s0, t0, TotalisFire
    li t0, 4
    beq s0, t0, TotalisFire

    li t0, 5
    beq s0, t0, TotalisEarth
    li t0, 6
    beq s0, t0, TotalisEarth

    li t0, 7
    beq s0, t0, TotalisMetal
    li t0, 8
    beq s0, t0, TotalisMetal

    li t0, 9
    beq s0, t0, TotalisWater
    li t0, 0
    beq s0, t0, TotalisWater
    ret

SkyisWood:
    li s5, 64
    ret
SkyisFire:
    li s5, 65
    ret
SkyisEarth:
    li s5, 66
    ret
SkyisMetal:
    li s5, 67
    ret
SkyisWater:
    li s5, 68
    ret

PeopleisWood:
    li s6, 64
    ret
PeopleisFire:
    li s6, 65
    ret
PeopleisEarth:
    li s6, 66
    ret
PeopleisMetal:
    li s6, 67
    ret
PeopleisWater:
    li s6, 68
    ret

LandisWood:
    li s7, 64
    ret
LandisFire: 
    li s7, 65
    ret
LandisEarth:   
    li s7, 66
    ret     
LandisMetal:   
    li s7, 67
    ret
LandisWater:    
    li s7, 68
    ret

OutsideisWood:
    li s8, 64
    ret
OutsideisFire:  
    li s8, 65
    ret
OutsideisEarth:
    li s8, 66
    ret 
OutsideisMetal:
    li s8, 67
    ret
OutsideisWater:
    li s8, 68
    ret

TotalisWood:
    li s9, 64
    ret
TotalisFire:
    li s9, 65
    ret
TotalisEarth:
    li s9, 66
    ret
TotalisMetal:   
    li s9, 67
    ret
TotalisWater:
    li s9, 68
    ret

CheckSEP:
    beq s5, s6, printSkyEqualPeople
    ret

CheckSEL:
    beq s5, s7, printSkyEqualLand
    ret

CheckSEO:
    beq s5, s8, printSkyEqualOutside
    ret

CheckSET:
    beq s5, s9, printSkyEqualTotal
    ret

CheckSGP:
    li t0, 1
    mv t1 , s5
    add t0, t1, t0
    beq t0, s6, printSkyGeneratePeople

    li t0, 4
    sub t0, s5, t0
    beq t0, s6, printSkyGeneratePeople
    ret

CheckSGL:
    li t0, 1
    mv t1 , s5
    add t0, t1, t0
    beq t0, s7, printSkyGenerateLand

    li t0, 4
    sub t0, s5, t0
    beq t0, s7, printSkyGenerateLand
    ret

CheckSGO:
    li t0, 1
    mv t1 , s5
    add t0, t1, t0
    beq t0, s8, printSkyGenerateOutside

    li t0, 4
    sub t0, s5, t0
    beq t0, s8, printSkyGenerateOutside
    ret

CheckSGT:
    li t0, 1
    mv t1 , s5
    add t0, t1, t0
    beq t0, s9, printSkyGenerateTotal

    li t0, 4
    sub t0, s5, t0
    beq t0, s9, printSkyGenerateTotal
    ret

CheckSRP:
    li t0, 2
    mv t1 , s5
    add t0, t1, t0
    beq t0, s6, printSkyRestraintPeople

    li t0, 3
    sub t0, s5, t0
    beq t0, s6, printSkyRestraintPeople
    ret

CheckSRL:
    li t0, 2
    mv t1 , s5
    add t0, t1, t0
    beq t0, s7, printSkyRestraintPeople

    li t0, 3
    sub t0, s5, t0
    beq t0, s7, printSkyRestraintPeople
    ret

CheckSRO:
    li t0, 2
    mv t1 , s5
    add t0, t1, t0
    beq t0, s8, printSkyRestraintPeople

    li t0, 3
    sub t0, s5, t0
    beq t0, s8, printSkyRestraintPeople
    ret

CheckSRT:
    li t0, 2
    mv t1 , s5
    add t0, t1, t0
    beq t0, s9, printSkyRestraintPeople

    li t0, 3
    sub t0, s5, t0
    beq t0, s9, printSkyRestraintPeople
    ret

printSkyEqualPeople: 
    la a0, SEP
    li a7, 4			
    ecall
    ret

printSkyEqualLand:
    la a0, SEL
    li a7, 4
    ecall
    ret

printSkyEqualOutside:
    la a0, SEO
    li a7, 4
    ecall
    ret

printSkyEqualTotal:
    la a0, SET
    li a7, 4
    ecall
    ret

printSkyGeneratePeople:
    la a0, SGP
    li a7, 4
    ecall
    ret

printSkyGenerateLand:
    la a0, SGL
    li a7, 4
    ecall
    ret

printSkyGenerateOutside:
    la a0, SGO
    li a7, 4
    ecall
    ret

printSkyGenerateTotal:
    la a0, SGT
    li a7, 4
    ecall
    ret

printSkyRestraintPeople:
    la a0, SRP
    li a7, 4
    ecall
    ret

printSkyRestraintLand:
    la a0, SRL
    li a7, 4
    ecall
    ret

printSkyRestraintOutside:  
    la a0, SRO
    li a7, 4
    ecall
    ret

printSkyRestraintTotal:
    la a0, SRT
    li a7, 4
    ecall
    ret

CheckPEL:
    beq s6, s7, printPeopleEqualLand
    ret

CheckPEO:
    beq s6, s8, printPeopleEqualOutside
    ret

CheckPET:
    beq s6, s9, printPeopleEqualTotal
    ret

CheckPGS:
    li t0, 1
    mv t1 , s6
    add t0, t1, t0
    beq t0, s5, printPeopleGenerateSky

    li t0, 4
    sub t0, s6, t0
    beq t0, s5, printPeopleGenerateSky
    ret

CheckPGL:
    li t0, 1
    mv t1 , s6
    add t0, t1, t0
    beq t0, s7, printPeopleGenerateLand

    li t0, 4
    sub t0, s6, t0
    beq t0, s7, printPeopleGenerateLand
    ret

CheckPGO:
    li t0, 1
    mv t1 , s6
    add t0, t1, t0
    beq t0, s8, printPeopleGenerateOutside

    li t0, 4
    sub t0, s6, t0
    beq t0, s8, printPeopleGenerateOutside
    ret

CheckPGT:
    li t0, 1
    mv t1 , s6
    add t0, t1, t0
    beq t0, s9, printPeopleGenerateTotal

    li t0, 4
    sub t0, s6, t0
    beq t0, s9, printPeopleGenerateTotal
    ret

CheckPRS:   
    li t0, 2
    mv t1 , s6
    add t0, t1, t0
    beq t0, s5, printPeopleRestraintSky

    li t0, 3
    sub t0, s6, t0
    beq t0, s5, printPeopleRestraintSky
    ret

CheckPRL:
    li t0, 2
    mv t1 , s6
    add t0, t1, t0
    beq t0, s7, printPeopleRestraintLand

    li t0, 3
    sub t0, s6, t0
    beq t0, s7, printPeopleRestraintLand
    ret

CheckPRO:
    li t0, 2
    mv t1 , s6
    add t0, t1, t0
    beq t0, s8, printPeopleRestraintOutside

    li t0, 3
    sub t0, s6, t0
    beq t0, s8, printPeopleRestraintOutside
    ret

CheckPRT:
    li t0, 2
    mv t1 , s6
    add t0, t1, t0
    beq t0, s9, printPeopleRestraintTotal

    li t0, 3
    sub t0, s6, t0
    beq t0, s9, printPeopleRestraintTotal
    ret

printPeopleEqualLand:
    la a0, PEL
    li a7, 4
    ecall
    ret
    
printPeopleEqualOutside:
    la a0, PEO
    li a7, 4
    ecall
    ret
   
printPeopleEqualTotal:
    la a0, PET
    li a7, 4
    ecall
    ret

printPeopleGenerateSky:
    la a0, PGS
    li a7, 4
    ecall
    ret

printPeopleGenerateLand:
    la a0, PGL
    li a7, 4
    ecall
    ret

printPeopleGenerateOutside:
    la a0, PGO
    li a7, 4
    ecall
    ret

printPeopleGenerateTotal:
    la a0, PGT
    li a7, 4
    ecall
    ret

printPeopleRestraintSky:
    la a0, PRS
    li a7, 4
    ecall
    ret

printPeopleRestraintLand:
    la a0, PRL
    li a7, 4
    ecall
    ret
    
printPeopleRestraintOutside:
    la a0, PRO
    li a7, 4
    ecall
    ret

printPeopleRestraintTotal:
    la a0, PRT
    li a7, 4
    ecall
    ret
    
CheckLEO:
    beq s7, s8, printLandEqualOutside
    ret

CheckLET:
    beq s7, s9, printLandEqualTotal
    ret

CheckLGS:
    li t0, 1
    mv t1 , s7
    add t0, t1, t0
    beq t0, s5, printLandGenerateSky

    li t0, 4
    sub t0, s7, t0
    beq t0, s5, printLandGenerateSky
    ret

CheckLGP:
    li t0, 1
    mv t1 , s7
    add t0, t1, t0
    beq t0, s6, printLandGeneratePeople

    li t0, 4
    sub t0, s7, t0
    beq t0, s6, printLandGeneratePeople
    ret

CheckLGO:
    li t0, 1
    mv t1 , s7
    add t0, t1, t0
    beq t0, s8, printLandGenerateOutside

    li t0, 4
    sub t0, s7, t0
    beq t0, s8, printLandGenerateOutside
    ret

CheckLGT:
    li t0, 1
    mv t1 , s7
    add t0, t1, t0
    beq t0, s9, printLandGenerateTotal

    li t0, 4
    sub t0, s7, t0
    beq t0, s9, printLandGenerateTotal
    ret

CheckLRS:
    li t0, 2
    mv t1 , s7
    add t0, t1, t0
    beq t0, s5, printPeopleRestraintSky

    li t0, 3
    sub t0, s7, t0
    beq t0, s5, printPeopleRestraintSky
    ret

CheckLRP:
    li t0, 2
    mv t1 , s7
    add t0, t1, t0
    beq t0, s6, printLandRestraintPeople

    li t0, 3
    sub t0, s7, t0
    beq t0, s6, printLandRestraintPeople
    ret

CheckLRO:
    li t0, 2
    mv t1 , s7
    add t0, t1, t0
    beq t0, s8, printLandRestraintOutside

    li t0, 3
    sub t0, s7, t0
    beq t0, s8, printLandRestraintOutside
    ret

CheckLRT:
    li t0, 2
    mv t1 , s7
    add t0, t1, t0
    beq t0, s9, printLandRestraintTotal

    li t0, 3
    sub t0, s7, t0
    beq t0, s9, printLandRestraintTotal
    ret

printLandEqualOutside:
    la a0, LEO
    li a7, 4
    ecall
    ret

printLandEqualTotal:
    la a0, LET
    li a7, 4
    ecall
    ret

printLandGenerateSky:
    la a0, LGS
    li a7, 4
    ecall
    ret

printLandGeneratePeople:
    la a0, LGP
    li a7, 4
    ecall
    ret
    
printLandGenerateOutside:
    la a0, LGO
    li a7, 4
    ecall
    ret

printLandGenerateTotal:
    la a0, LGT
    li a7, 4
    ecall
    ret

printLandRestraintSky:
    la a0, LRS
    li a7, 4
    ecall
    ret

printLandRestraintPeople:
    la a0, LRP
    li a7, 4
    ecall
    ret

printLandRestraintOutside:
    la a0, LRO
    li a7, 4
    ecall
    ret

printLandRestraintTotal:
    la a0, LRT
    li a7, 4
    ecall
    ret

CheckOET:
    beq s8, s9, printOutsideEqualTotal
    ret

CheckOGS:
    li t0, 1
    mv t1 , s8
    add t0, t1, t0
    beq t0, s5, printOutsideGenerateSky

    li t0, 4
    sub t0, s8, t0
    beq t0, s5, printOutsideGenerateSky
    ret

CheckOGP:
    li t0, 1
    mv t1 , s8
    add t0, t1, t0
    beq t0, s6, printOutsideGeneratePeople

    li t0, 4
    sub t0, s8, t0
    beq t0, s6, printOutsideGeneratePeople
    ret

CheckOGL:
    li t0, 1
    mv t1 , s8
    add t0, t1, t0
    beq t0, s7, printOutsideGenerateLand

    li t0, 4
    sub t0, s8, t0
    beq t0, s7, printOutsideGenerateLand
    ret

CheckOGT:
    li t0, 1
    mv t1 , s8
    add t0, t1, t0
    beq t0, s9, printOutsideGenerateTotal

    li t0, 4
    sub t0, s8, t0
    beq t0, s9, printOutsideGenerateTotal
    ret

CheckORS:
    li t0, 2
    mv t1 , s8
    add t0, t1, t0
    beq t0, s5, printOutsideRestraintSky

    li t0, 3
    sub t0, s8, t0
    beq t0, s5, printOutsideRestraintSky
    ret

CheckORP:
    li t0, 2
    mv t1 , s8
    add t0, t1, t0
    beq t0, s6, printOutsideRestraintPeople

    li t0, 3
    sub t0, s8, t0
    beq t0, s6, printOutsideRestraintPeople
    ret

CheckORL:
    li t0, 2
    mv t1 , s8
    add t0, t1, t0
    beq t0, s7, printOutsideRestraintLand

    li t0, 3
    sub t0, s8, t0
    beq t0, s7, printOutsideRestraintLand
    ret

CheckORT:
    li t0, 2
    mv t1 , s8
    add t0, t1, t0
    beq t0, s9, printOutsideRestraintTotal

    li t0, 3
    sub t0, s8, t0
    beq t0, s9, printOutsideRestraintTotal
    ret

printOutsideEqualTotal:
    la a0, OET
    li a7, 4
    ecall
    ret

printOutsideGenerateSky:
    la a0, OGS
    li a7, 4
    ecall
    ret

printOutsideGeneratePeople:
    la a0, OGP
    li a7, 4
    ecall
    ret

printOutsideGenerateLand:
    la a0, OGL
    li a7, 4
    ecall
    ret

printOutsideGenerateTotal:
    la a0, OGT
    li a7, 4
    ecall
    ret

printOutsideRestraintSky:
    la a0, ORS
    li a7, 4
    ecall
    ret

printOutsideRestraintPeople:
    la a0, ORP
    li a7, 4
    ecall
    ret

printOutsideRestraintLand:
    la a0, ORL
    li a7, 4
    ecall
    ret

printOutsideRestraintTotal:
    la a0, ORT
    li a7, 4
    ecall
    ret

CheckTGS:
    li t0, 1
    mv t1 , s9
    add t0, t1, t0
    beq t0, s5, printOutsideGenerateSky

    li t0, 4
    sub t0, s9, t0
    beq t0, s5, printOutsideGenerateSky
    ret

CheckTGP:
    li t0, 1
    mv t1 , s9
    add t0, t1, t0
    beq t0, s6, printTotalGeneratePeople

    li t0, 4
    sub t0, s9, t0
    beq t0, s6, printTotalGeneratePeople
    ret

CheckTGL:
    li t0, 1
    mv t1 , s9
    add t0, t1, t0
    beq t0, s7, printTotalGenerateLand

    li t0, 4
    sub t0, s9, t0
    beq t0, s7, printTotalGenerateLand
    ret

CheckTGO:
    li t0, 1
    mv t1 , s9
    add t0, t1, t0
    beq t0, s8, printTotalGenerateOutside

    li t0, 4
    sub t0, s9, t0
    beq t0, s8, printTotalGenerateOutside
    ret

CheckTRS:
    li t0, 2
    mv t1 , s9
    add t0, t1, t0
    beq t0, s5, printTotalRestraintSky

    li t0, 3
    sub t0, s9, t0
    beq t0, s5, printTotalRestraintSky
    ret

CheckTRP:
    li t0, 2
    mv t1 , s9
    add t0, t1, t0
    beq t0, s6, printTotalRestraintPeople

    li t0, 3
    sub t0, s9, t0
    beq t0, s6, printTotalRestraintPeople
    ret

CheckTRL:
    li t0, 2
    mv t1 , s9
    add t0, t1, t0
    beq t0, s7, printTotalRestraintLand

    li t0, 3
    sub t0, s9, t0
    beq t0, s7, printTotalRestraintLand
    ret

CheckTRO:
    li t0, 2
    mv t1 , s9
    add t0, t1, t0
    beq t0, s8, printTotalRestraintOutside

    li t0, 3
    sub t0, s9, t0
    beq t0, s8, printTotalRestraintOutside
    ret

printTotalGenerateSky:
    la a0, TGS
    li a7, 4
    ecall
    ret

printTotalGeneratePeople:
    la a0, TGP
    li a7, 4
    ecall
    ret

printTotalGenerateLand: 
    la a0, TGL
    li a7, 4
    ecall
    ret

printTotalGenerateOutside:
    la a0, TGO
    li a7, 4
    ecall
    ret

printTotalRestraintSky:
    la a0, TRS
    li a7, 4
    ecall
    ret

printTotalRestraintPeople:
    la a0, TRP
    li a7, 4
    ecall
    ret

printTotalRestraintLand:
    la a0, TRL
    li a7, 4
    ecall
    ret

printTotalRestraintOutside:
    la a0, TRO
    li a7, 4
    ecall
    ret

PrintElement:
    #s0 = s0 mod 10
    li t0, 10
    rem s0, s0, t0

    # if s0 is 1 or 2, print Wood
    li t0, 1
    beq s0, t0, printWood
    li t0, 2
    beq s0, t0, printWood

    # if s0 is 3 or 4, print Fire
    li t0, 3
    beq s0, t0, printFire
    li t0, 4
    beq s0, t0, printFire

    # if s0 is 5 or 6, print Earth
    li t0, 5
    beq s0, t0, printEarth
    li t0, 6
    beq s0, t0, printEarth

    # if s0 is 7 or 8, print Metal
    li t0, 7
    beq s0, t0, printMetal
    li t0, 8
    beq s0, t0, printMetal

    # if s0 is 9 or 0, print Water
    li t0, 9
    beq s0, t0, printWater
    li t0, 0
    beq s0, t0, printWater
    ret

printResult:
	mv a0,s0
	li a7, 1	
 	ecall
 	ret
printNewLine:
    li a0, 10   # ASCII value for newline
    li a7, 11   # print character
    ecall
 	ret
printEqualSign:
    la a0, equalSign
    li a7, 4
    ecall
    ret

end:
	li a7, 10			
 	ecall
