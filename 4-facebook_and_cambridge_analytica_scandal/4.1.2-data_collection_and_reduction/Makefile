


all: collectComments parseComments

# collect all the data from the youtube comments.
collectComments: 6ValJMOpt7s hJdxOqnCNp8 BylLTX05jSY snDGFwvLVm8 Ziw70UJLVHc \
CMZTbMFK5eA mZaec_mlq9M H-paF1w8_y8 cyJosQBtzsw _Te_LKt5DpY

# parse all collected data into a single csv file with specific rows
# extracted.
parseComments:
	python parseComments.py data/comments/ --out=data/comments/comments.csv

# washington post day 1
6ValJMOpt7s:
	python getComments.py 6ValJMOpt7s --out=data/comments/6ValJMOpt7s.json
# washington post day 2
hJdxOqnCNp8:
	python getComments.py hJdxOqnCNp8 --out=data/comments/hJdxOqnCNp8.json
# NBC day 1
BylLTX05jSY:
	python getComments.py BylLTX05jSY --out=data/comments/BylLTX05jSY.json
# NBC day 2
snDGFwvLVm8:
	python getComments.py snDGFwvLVm8 --out=data/comments/snDGFwvLVm8.json
# Time day 1
Ziw70UJLVHc:
	python getComments.py Ziw70UJLVHc --out=data/comments/Ziw70UJLVHc.json
# Time day 2
CMZTbMFK5eA:
	python getComments.py CMZTbMFK5eA --out=data/comments/CMZTbMFK5eA.json
# The Guardian day 1
mZaec_mlq9M:
	python getComments.py mZaec_mlq9M --out=data/comments/mZaec_mlq9M.json
# The Guardian day 2
H-paF1w8_y8:
	python getComments.py H-paF1w8_y8 --out=data/comments/H-paF1w8_y8.json
# Bloomberg day 1
cyJosQBtzsw:
	python getComments.py cyJosQBtzsw --out=data/comments/cyJosQBtzsw.json
# Bloomberg day 2
_Te_LKt5DpY:
	python getComments.py _Te_LKt5DpY --out=data/comments/_Te_LKt5DpY.json


# remove all json files in the data dir.
clean:
	find data/ -type f -name '*.json' -delete