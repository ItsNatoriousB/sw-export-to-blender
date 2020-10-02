-- Originally made by TGE to rip mesh and texture data, with rudimentary bone support
-- Modified by TwiliChaos to fix bone support, add skinning support, and add animation support

global importNormals = true
useMaya = true

st  = 0 
et  = 0
dst = 0
det = 0
ast = 0
aet = 0

viewport.setRenderLevel #flat

clearlistener()
fname = getOpenFileName \
caption:"Open Model" \
types:"Summoners War Model (*.dat)|*.dat" \
historyCategory:"SWM Object Presets"

f = fopen fname "rb"
fileName = GetFilenameFile fname
filePath = getFileNamePath fname

print ("Opened file " + fileName)

fseek f 0 #seek_end
fileEnd = ftell f
fseek f 0 #seek_set

-- -------------------------------------------------------------------------------------------------------------- Header
headerSize = readlong f

fseek f 0xE #seek_cur
EncryptCheck = readbyte f
DoDecrypt = false
DoAnimationData = false
if (EncryptCheck == 0x4F) then -- Decrypt the file
(
	DoDecrypt = true
	dst = timestamp()
    com2us_decrypt_values = #(
        0x2f, 0x7c, 0x47, 0x55, 0x32, 0x77, 0x9f, 0xfb, 0x5b, 0x86, 0xfe, 0xb6, 0x3e, 0x06, 0xf4, 0xc4,
        0x2e, 0x08, 0x49, 0x11, 0x0e, 0xce, 0x84, 0xd3, 0x7b, 0x18, 0xa6, 0x5c, 0x71, 0x56, 0xe2, 0x3b,
        0xfd, 0xb3, 0x2b, 0x97, 0x9d, 0xfc, 0xca, 0xba, 0x8e, 0x7e, 0x6f, 0x0f, 0xe8, 0xbb, 0xc7, 0xc2,
        0xd9, 0xa4, 0xd2, 0xe0, 0xa5, 0x95, 0xee, 0xab, 0xf3, 0xe4, 0xcb, 0x63, 0x25, 0x70, 0x4e, 0x8d,
        0x21, 0x37, 0x9a, 0xb0, 0xbc, 0xc6, 0x48, 0x3f, 0x23, 0x80, 0x20, 0x01, 0xd7, 0xf9, 0x5e, 0xec,
        0x16, 0xd6, 0xd4, 0x1f, 0x51, 0x42, 0x6c, 0x10, 0x14, 0xb7, 0xcc, 0x82, 0x7f, 0x13, 0x02, 0x00,
        0x72, 0xed, 0x90, 0x57, 0xc1, 0x2c, 0x5d, 0x28, 0x81, 0x1d, 0x38, 0x1a, 0xac, 0xad, 0x35, 0x78,
        0xdc, 0x68, 0xb9, 0x8b, 0x6a, 0xe1, 0xc3, 0xe3, 0xdb, 0x6d, 0x04, 0x27, 0x9c, 0x64, 0x5a, 0x8f,
        0x83, 0x0c, 0xd8, 0xa8, 0x1c, 0x89, 0xd5, 0x43, 0x74, 0x73, 0x4d, 0xae, 0xea, 0x31, 0x6e, 0x1e,
        0x91, 0x1b, 0x59, 0xc9, 0xbd, 0xf7, 0x07, 0xe7, 0x8a, 0x05, 0x8c, 0x4c, 0xbe, 0xc5, 0xdf, 0xe5,
        0xf5, 0x2d, 0x4b, 0x76, 0x66, 0xf2, 0x50, 0xd0, 0xb4, 0x85, 0xef, 0xb5, 0x3c, 0x7d, 0x3d, 0xe6,
        0x9b, 0x03, 0x0d, 0x61, 0x33, 0xf1, 0x92, 0x53, 0xff, 0x96, 0x09, 0x67, 0x69, 0x44, 0xa3, 0x4a,
        0xaf, 0x41, 0xda, 0x54, 0x46, 0xd1, 0xfa, 0xcd, 0x24, 0xaa, 0x88, 0xa7, 0x19, 0xde, 0x40, 0xeb,
        0x94, 0x5f, 0x45, 0x65, 0xf0, 0xb8, 0x34, 0xdd, 0x0b, 0xb1, 0x29, 0xe9, 0x2a, 0x75, 0x87, 0x39,
        0xcf, 0x79, 0x93, 0xa1, 0xb2, 0x30, 0x15, 0x7a, 0x52, 0x12, 0x62, 0x36, 0xbf, 0x22, 0x4f, 0xc0,
        0xa2, 0x17, 0xc8, 0x99, 0x3a, 0x60, 0xa9, 0xa0, 0x58, 0xf6, 0x0a, 0x9e, 0xf8, 0x6b, 0x26, 0x98
    )
    fseek f (headerSize + 0x4) #seek_set
    PMMSize = readlong f
    fseek f 0 #seek_set

    print ("This file is encrypted. Creating decrypted file. This may take around a minute.")
    dname = (filePath + fileName + "_dec.dat")
    copyFile fname dname
    d = fopen dname "wb" -- Overwrites encryption values to be decrypted

    for i = 1 to 17 do (writebyte d (readbyte f))
    writebyte d 0x23
    writebyte d 0x5A
    fseek f 2 #seek_cur
    for i = 1 to (headerSize - 11) do writebyte d (readbyte f)
    for i = 1 to (PMMSize) do writebyte d com2us_decrypt_values[(readbyte f #unsigned) + 1]
    while (not (ftell f >= fileEnd)) do writebyte d (readbyte f)
    fclose d
	fclose f
	f = fopen dname "rb"
	fname = dname

	fileName = GetFilenameFile fname
	filePath = getFileNamePath fname

    print ("File decrypted. Now using " + fname ". For future uses of this model file, please use this _dec version.")
	det = timestamp()
)
/*if (EncryptCheck != 0x5A23 and EncryptCheck != 0x4F73) then print ("Unknown encryption value " + (intToHexString EncryptCheck) + ", expected 5A23 or 4F73")
else */
with undo off (
	st = timestamp()
	fseek f (headerSize + 0x4) #seek_set
	PMMSize = readlong f
	fseek f 4 #seek_cur

	-- -------------------------------------------------------------------------------------------------------------- PMM$ / Mesh Data
	unk1 = readshort f
	faceCount = readshort f #unsigned / 3
	vertCount = readshort f #unsigned
	unk2 = readlong f
	vertScale = readshort f #unsigned

	fseek f 0x37 #seek_cur
	print ("Getting mesh data...")
	vertArray = #()
	for v = 1 to vertCount do
	(
		vx = readlong f as float / vertScale
		vy = readlong f as float / vertScale
		vz = readlong f as float / vertScale
		append vertArray [vx,-vz,vy]
	)
	normArray = #()
	for v = 1 to vertCount do
	(
		nx = readbyte f as float / 0x7F
		ny = readbyte f as float / 0x7F
		nz = readbyte f as float / 0x7F
		append normArray [nx,nz,ny]
	)
	uvArray = #()
	for v = 1 to vertCount do
	(
		tu = readlong f as float / 0xFFFF
		tv = readlong f as float / 0xFFFF
		append uvArray [tu,tv,0]
	)
	faceArray = #()
	for fc = 1 to faceCount do
	(
		f1 = readshort f #unsigned + 1
		f2 = readshort f #unsigned + 1
		f3 = readshort f #unsigned + 1
		append faceArray [f1,f2,f3]
	)

	boneIDArray = #()
	for v = 1 to vertCount do append boneIDArray (readbyte f #unsigned +1)
	-- -------------------------------------------------------------------------------------------------------------- PLM$ / Rigging
	print("Getting armature data...")
	PLMSize = readlong f
	PLMStart = ftell f
	fseek f 4 #seek_cur
	AnimTrackCount = readshort f
	AnimTrackHeaderData = ftell f
	trackSize = #()
	fseek f 0x14 #seek_cur
	for i = 1 to AnimTrackCount do
	(
		fseek f 0x5 #seek_cur
		append trackSize (int(readshort f #unsigned))
	)
	boneCount = readbyte f #unsigned
	fseek f 0x20 #seek_cur -- Quaternion is 8 bytes, Position is 12, Scale is 12, 32 is skipped... what could this be?

	boneArray = #()
	for b = 1 to boneCount do
	(
		boneFlag = readbyte f
		boneID = readbyte f #unsigned
		parentID = readbyte f #unsigned
		StartPos = ftell f
		unk4 = readlong f
		q1 = readshort f as float / 0x7FFF
		q2 = readshort f as float / 0x7FFF
		q3 = readshort f as float / 0x7FFF
		q4 = readshort f as float / 0x7FFF
		p1 = readlong f as float / vertScale
		p2 = readlong f as float / vertScale
		p3 = readlong f as float / vertScale
		s1 = readlong f as float / 0x10000
		s2 = readlong f as float / 0x10000
		s3 = readlong f as float / 0x10000

		if boneID == 0 then s2 = -s2

		tfm = quat q1 q3 q2 q4 as matrix3
		tfm.row4 = [p1,p3,p2]
		tfm *= (scalematrix [s1,s2,s3])

		boneName = ("Bone"+(b as string))

		if ((getNodeByName boneName) != undefined) do (append boneArray (getNodeByName boneName))
		if (parentID < boneCount) then (tfm = tfm * boneArray[parentID+1].objecttransform)

		newBone = bonesys.createbone	\
						tfm.row4	\
						(tfm.row4 + 0.01 * (normalize tfm.row1)) \
						(normalize tfm.row3)
					newBone.name = boneName
					newBone.width  = 0.001
					newBone.height = 0.001
					newBone.transform = tfm
					newBone.setBoneEnable false 0
					newBone.wirecolor = yellow
					newbone.showlinks = true
					newBone.pos.controller      = TCB_position ()
					newBone.rotation.controller = TCB_rotation ()
		if boneFlag != -1 then (
			newBone.wirecolor = red -- Likely not bound to skin and should be highlighted as possibly unimportant
			newBone.name += ("_Flag_" + boneFlag as string)
		)
		if (parentID < boneCount) then newBone.parent = boneArray[(parentID+1)]
		append boneArray newBone
	)
	AnimStart = ftell f
	-------------------------------------------------------------------------------------------------------------- Textures
	fseek f (PLMStart + PLMSize) #seek_set

	if (doesFileExist (filepath + filename + "_textures" + "\\")) == false then
	(
		print ("Getting textures...")
		while (not (ftell f >= fileEnd)) do
		(
			elementID = readlong f
			textureSize = readlong f
			if textureSize > 0 then print ("Texture " + elementID as string + " is of size " + textureSize as string) else print ("Texture " + elementID as string + " is empty")
			pngData = #()
			pngName = (filepath + fileName + "_textures" + "\\" + fileName + "_" + elementID as string + ".png")
			makeDir (filepath + fileName + "_textures" + "\\")
			if (textureSize != 0) then
			(
				for i = 1 to textureSize do pngData[i] = (readbyte f)
				png = createfile pngName
				close png
				png = fopen pngName "wb"
				for i = 1 to textureSize do writebyte png pngData[i]
				fclose png
			)
		)
	) else print ("Skipping textures since they already exist.")

	-------------------------------------------------------------------------------------------------------------- Mesh Creation
	print ("Creating mesh...")
	msh = mesh vertices:vertArray faces:faceArray
	msh.name = filename
	msh.numTVerts = vertArray.count
	buildTVFaces msh
	for j = 1 to uvArray.count do setTVert msh j uvArray[j]
	for j = 1 to faceArray.count do setTVFace msh j faceArray[j]
	for j = 1 to msh.numfaces do setFaceSmoothGroup msh j 1
	for j = 1 to msh.numfaces do setFaceMatID msh j 1

	if ((normArray.count != 0) AND (importNormals == true)) then (
		max modify mode
		select msh
		addmodifier msh (Edit_Normals ()) ui:off
		msh.Edit_Normals.MakeExplicit selection:#{1..normArray.count}
		EN_convertVS = msh.Edit_Normals.ConvertVertexSelection
		EN_setNormal = msh.Edit_Normals.SetNormal
		normID = #{}

		for v = 1 to normArray.count do(
				free normID
				EN_convertVS #{v} &normID
				for id in normID do EN_setNormal id normArray[v]
		)
	)
	maxOps.CollapseNodeTo msh 1 true -- Collapse the Edit Normals modifier

	msh.material = Standard()
	useTexture = 1
	if      (doesFileExist (filepath + fileName + "_textures" + "\\" + fileName + "_1.png")) then useTexture = 1
	else if (doesFileExist (filepath + fileName + "_textures" + "\\" + fileName + "_2.png")) then useTexture = 2
	else if (doesFileExist (filepath + fileName + "_textures" + "\\" + fileName + "_3.png")) then useTexture = 3
	else if (doesFileExist (filepath + fileName + "_textures" + "\\" + fileName + "_4.png")) then useTexture = 4
	else if (doesFileExist (filepath + fileName + "_textures" + "\\" + fileName + "_5.png")) then useTexture = 5
	else useTexture = 6

	tm = Bitmaptexture filename:(filepath + fileName + "_textures" + "\\" + fileName + "_" + useTexture as string + ".png")
	msh.material.diffuseMap = tm
	msh.material.ShowInViewport = true


	-------------------------------------------------------------------------------------------------------------- Skinning

	skn = Skin()
	addmodifier msh skn
	max modify mode

	for b = 1 to boneCount do skinOps.addBone skn boneArray[b] 0
	for v = 1 to msh.numVerts do skinOps.ReplaceVertexWeights skn v boneIDArray[v] 1

	boneArray[1].transform *= (scalematrix [1,-1,1])
	et = timestamp()
	-------------------------------------------------------------------------------------------------------------- Animation Data

	if queryBox "Finished grabbing mesh, armature, and texture data.\nDo you want to attempt to grab animations?\nThis process is expected to take at least a minute." beep:true then
	(
		print ("Getting animation data...")
		fn byteToBitArray theByte origBitArray = (
			theBitArray = origBitArray
			for i = 1 to 8 do append theBitArray (bit.get theByte i)
			return theBitArray
		)
		DoAnimationData = true
		ast = timestamp()

		format ("Track count: " + AnimTrackCount as string + ", Bone count: " + boneCount as string + "\nTrack lengths --- ")
		for i = 1 to AnimTrackCount do format (i as string + ": [" + trackSize[i] as string + "] ")
		format "\n"

		fseek f AnimStart #seek_set

		trackStartPos = #()
		trackEndPos = #()
		start = 1
		end = 0
		for i = 1 to AnimTrackCount do
		(
			if i > 1 then start = end + 1
			end = start + trackSize[i] - 1
			append trackStartPos start
			append trackEndPos end
		)
		for i = 1 to AnimTrackCount do -- Loop through each track
		(
			HeaderSize = int(ceil (trackSize[i] / 8 + 1))
			fseek f 0x18 #seek_cur
			for j = 1 to boneCount do		-- loop through each bone in track
			(
				quatKeyCount = 1
				posKeyCount = 1
				scaleKeyCount = 1

				quatBitArray = #()
				posBitArray = #()
				scaleBitArray = #()

				quatArray = #()
				posArray = #()
				scaleArray = #()

				if int(readbyte f #unsigned) != 0 then							-- Quat header
				(
					fseek f -1 #seek_cur
					quatKeyCount = 0
					for k = 1 to HeaderSize do
					(
						HeaderVal = (readbyte f #unsigned)
						quatBitArray = (byteToBitArray HeaderVal quatBitArray)
					)
					for l = 1 to trackSize[i] do if quatBitArray[l] then quatKeyCount += 1 -- to trackSize, NOT quatBitArray.count
				)
				else
				(
					append quatBitArray true
					for k = 2 to trackSize[i] do append quatBitArray false
				)

				for k = 1 to quatKeyCount do									-- Quat keyframes
				(
					q1 = readshort f as float / 0x7FFF
					q2 = readshort f as float / 0x7FFF
					q3 = readshort f as float / 0x7FFF
					q4 = readshort f as float / 0x7FFF

					append quatArray (quat q1 q3 q2 q4)
				)
				if int(readbyte f #unsigned) != 0 then							-- Pos header
				(
					fseek f -1 #seek_cur
					posKeyCount = 0
					for k = 1 to HeaderSize do
					(
						HeaderVal = (readbyte f #unsigned)
						posBitArray = (byteToBitArray HeaderVal posBitArray)
					)
					for l = 1 to trackSize[i] do if posBitArray[l] then posKeyCount += 1 -- to trackSize, NOT posBitArray.count
				)
				else
				(
					append posBitArray true
					for k = 2 to trackSize[i] do append posBitArray false
				)

				for k = 1 to posKeyCount do										-- Pos keyframes
				(
					p1 = readlong f as float / vertScale
					p2 = readlong f as float / vertScale
					p3 = readlong f as float / vertScale

					append posArray [p1,p3,p2]
				)
				if int(readbyte f #unsigned) != 0 then							-- Scale header
				(
					fseek f -1 #seek_cur
					scaleKeyCount = 0
					for k = 1 to HeaderSize do
					(
						HeaderVal = (readbyte f #unsigned)
						scaleBitArray = (byteToBitArray HeaderVal scaleBitArray)
					)
					for l = 1 to trackSize[i] do if scaleBitArray[l] then scaleKeyCount += 1 -- to trackSize, NOT scaleBitArray.count
				)
				else
				(
					append scaleBitArray true
					for k = 2 to trackSize[i] do append scaleBitArray false
				)

				for k = 1 to scaleKeyCount do 									-- Scale keyframes
				(
					s1 = readlong f as float / 0x10000
					s2 = readlong f as float / 0x10000
					s3 = readlong f as float / 0x10000

					append scaleArray [s3,s1,s2]
				)

				QuatTime = trackStartPos[i]
				PosTime = trackStartPos[i]
				ScaleTime = trackStartPos[i]
				
				p = boneArray[j].parent

				quatBitPos = 0
				posBitPos = 0
				scaleBitPos = 0
				
				for k = 1 to QuatKeyCount do									-- Apply Quaternion
				(
					b = false
					while b == false do
					(
						quatBitPos += 1
						b = quatBitArray[quatBitPos]
					)
					QuatTime = trackStartPos[i] + quatBitPos - 1
					
					tfm = quatArray[k] as matrix3
					keeppos = (at time QuatTime boneArray[j].transform.row4)
					tfm.row4 = keeppos
					if (p != undefined) then tfm *=(at time QuatTime p.objecttransform)
					with animate on at time QuatTime boneArray[j].transform = tfm
					selectKey boneArray[j].pos.controller boneArray[j].pos.controller.keys.count
					deleteKeys boneArray[j].pos.controller #selection
				)
				
				for k = 1 to PosKeyCount do										-- Apply Position
				(
					b = false
					while b == false do
					(
						posBitPos += 1
						b = posBitArray[posBitPos]
					)
					PosTime = trackStartPos[i] + posBitPos - 1
					
					tfm = ((at time (PosTime) boneArray[j].transform) as quat) as matrix3
					tfm_keepquat = tfm
					tfm.row4 = posArray[k]
					
					if (p != undefined) then tfm *= (at time PosTime p.objecttransform)
					tfm_keepquat.row4 = tfm.row4
					with animate on at time PosTime boneArray[j].transform = tfm_keepquat
					
					if quatBitArray[posBitPos] then doDeleteQuat = false else doDeleteQuat = true
					if doDeleteQuat then
					(
						selectKeys boneArray[j].rotation.controller PosTime PosTime
						deleteKeys boneArray[j].rotation.controller #selection
					)
				)
				
				for k = 1 to ScaleKeyCount do									-- Apply Scale
				(
					b = false
					while b == false do
					(
						scaleBitPos += 1
						b = scaleBitArray[scaleBitPos]
					)
					ScaleTime = trackStartPos[i] + scaleBitPos - 1
					with animate on at time ScaleTime
					(
						if p != undefined then in coordsys p scale boneArray[j] scaleArray[k]
										  else in coordsys world scale boneArray[j] scaleArray[k]
					)
				)
			)
			format ("Track " + i as string + " of " + AnimTrackCount as string + " complete\n")
		)
		animationRange = interval 0 trackEndPos[AnimTrackCount]

		if useMaya then (
			format ("If you use Maya, you can copy the below text into the MEL channel box:\n" +
			"//////////////////////////////////////////////////\n\n" +
			"currentUnit -time ntsc ;\n" +
			"playbackOptions -ps 1 ;\n" +
			"playbackOptions -e -min 1 -max " + trackEndPos[AnimTrackCount] as string + " ;\n" +
			"select -r -hi Bone1 ;\n" +
			"character -name " + fileName + "_chr ;\n")
			for i = 1 to trackSize.count do
			(
				format ("clip -s " + trackStartPos[i] as string + " -end " + trackEndPos[i] as string)
				--if i != trackSize.count then format " -lo"
				format (" -name \"Track_" + i as string + "\" \"" + fileName + "_chr\" ;\n")
				--print ("Track " + i as string + " starts at " + start as string + " and ends at " + end as string)
			)
			format "\n//////////////////////////////////////////////////"
		)
	)
)
-------------------------------------------------------------------------------------------------------------- End of model creation
format "\n\n"
aet = timestamp()
dtime = ((int((det as float - dst as float) / 10 )) as float) as float / 100
etime = ((int(( et as float -  st as float) / 10 )) as float) as float / 100
atime = ((int((aet as float - ast as float) / 10 )) as float) as float / 100

if DoDecrypt == true then print ("Decryption completed in " + dtime as string + " seconds.")
print ("Mesh, Armature, and Textures completed in " + etime as string + " seconds.")
if DoAnimationData == true then print ("Animations completed in " + atime as string + " seconds.")
fseek f fileEnd #seek_set
fclose f
gc()
