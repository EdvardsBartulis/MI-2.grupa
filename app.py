import tkinter as tk
import tkinter.font as tkFont
import math
import random
import sys
import os
import time


#Restartē spēli.
def RestartGame():
	python = sys.executable
	os.execl(python, python, *sys.argv)


#Atgriež piecus nejauši izveidotus skaitļus, kurus varēs izvēlēties spēles uzsākšanai.
def generate_root():
	root_array = []
	while len(root_array) < 5:
		root = random.randint(10000, 20000)
		if root % 2 == 0 and root % 3 == 0:
			root_array.append(root)
	return root_array


#Funkcija spēles koka izvadīšanai.
def print_speles_koku():
	for i in spk.virsotnu_kopa:
		print("ID: ", i.id, "Number: ", i.virkne, "P1: ", i.p1, "P2: ", i.p2,
		      "B: ", i.bank, "Lim: ", i.limenis)


#Izveido spēles koku.
def generate_tree(num):
	id_new = 'A'
	sakne = Virsotne(id_new + '0', num, 0, 0, 0, 1)
	undivided = []
	undivided.append(sakne)
	spk.pievienot_virsotni(sakne)
	j = 1
	newvirs = Virsotne(id_new, num, 0, 0, 0, 1)
	maxlim = 1

	while len(undivided) > 0:
		if (undivided[0].virkne % 2 == 0
		    and undivided[0].virkne > 10):  # dalas ar 2
			newnum = undivided[0].virkne // 2
			if newnum < 10:
				break

			if (undivided[0].limenis % 2 != 0):  # 1.speletajs
				newvirs = Virsotne(id_new + str(j), newnum, undivided[0].p1,
				                   undivided[0].p2 + 2, undivided[0].bank,
				                   undivided[0].limenis + 1)

			if (undivided[0].limenis % 2 == 0):  # 2.speletajs
				newvirs = Virsotne(id_new + str(j), newnum, undivided[0].p1 + 2,
				                   undivided[0].p2, undivided[0].bank,
				                   undivided[0].limenis + 1)

			if (newvirs.virkne % 5 == 0):  # vai bankai + 1?
				newvirs.bank = undivided[0].bank + 1

			if (newvirs.virkne % 2 != 0
			    and newvirs.virkne % 3 != 0) or newvirs.virkne <= 10:
				if (undivided[0].limenis % 2
				    != 0):  #ja 1.speletajs izdara pedejo gajenu
					newvirs.p1 = newvirs.p1 + newvirs.bank
					newvirs.bank = 0
				if (undivided[0].limenis %
				    2 == 0):  #ja 2.speletajs izdara pedejo gajenu
					newvirs.p2 = newvirs.p2 + newvirs.bank
					newvirs.bank = 0

			spk.pievienot_loku(undivided[0].id, newvirs.id)
			spk.pievienot_childloku(newvirs.id, undivided[0].id)
			j += 1
			undivided.append(newvirs)
			spk.pievienot_virsotni(newvirs)

		if (undivided[0].virkne % 3 == 0
		    and undivided[0].virkne > 10):  # dalas ar 3
			newnum = undivided[0].virkne // 3
			if newnum < 10:
				break

			if (undivided[0].limenis % 2 != 0):  #  1.speletajs
				newvirs = Virsotne(id_new + str(j), newnum, undivided[0].p1 + 3,
				                   undivided[0].p2, undivided[0].bank,
				                   undivided[0].limenis + 1)

			if (undivided[0].limenis % 2 == 0):  # 2.speletajs
				newvirs = Virsotne(id_new + str(j), newnum, undivided[0].p1,
				                   undivided[0].p2 + 3, undivided[0].bank,
				                   undivided[0].limenis + 1)

			if (newvirs.virkne % 5 == 0):  # vai bankai +1?
				newvirs.bank = undivided[0].bank + 1

			spk.pievienot_loku(undivided[0].id, newvirs.id)
			spk.pievienot_childloku(newvirs.id, undivided[0].id)
			if (newvirs.virkne % 2 != 0
			    and newvirs.virkne % 3 != 0) or newvirs.virkne <= 10:
				if (undivided[0].limenis % 2
				    != 0):  #ja 1.speletajs izdara pedejo gajenu
					newvirs.p1 = newvirs.p1 + newvirs.bank
					newvirs.bank = 0
				if (undivided[0].limenis %
				    2 == 0):  #ja 2.speletajs izdara pedejo gajenu
					newvirs.p2 = newvirs.p2 + newvirs.bank
					newvirs.bank = 0
			j += 1
			undivided.append(newvirs)
			spk.pievienot_virsotni(newvirs)
			maxlim = undivided[0].limenis

		undivided.pop(0)

	app.maxlim = maxlim
	app.strupvirs = get_strupvirs(spk)
	#print_speles_koku()
	return spk


#Min-max algoritma funkcija.
def min_max(spk, Virsotne, speletajs):
	if spk.loku_kopa.get(Virsotne.id) is None:
		print("Ievades kļūda, tāda virsitne neeksistē")
	else:
		bernu_masivs = spk.loku_kopa.get(Virsotne.id)  # priekš tekošai virsotnei

		if len(bernu_masivs) == 1:
			return spk.virsotnu_kopa[int(
			    bernu_masivs[0][1:])]  # ja ir tikai viena gājiens
		else:
			vardnica = dict()  # virsotnes id, kvalitāte
			# atrast koka pēdējo līmeni
			i = len(spk.virsotnu_kopa)  # A0....Ai-1
			max_limenis = spk.virsotnu_kopa[i - 1].limenis
			limenis = max_limenis
			kvalitate = 0

			while limenis >= Virsotne.limenis:
				for virsotne in spk.virsotnu_kopa:
					if virsotne.limenis == limenis:  # parbaude pa limenim

						if spk.loku_kopa.get(virsotne.id) == None:
							if virsotne.p1 > virsotne.p2:
								kvalitate = 1  # uzvara
							elif virsotne.p1 == virsotne.p2:
								kvalitate = 0  # neizšķirts
							else:
								kvalitate = -1  # zaudejums

						else:
							bernu_mas = spk.loku_kopa.get(virsotne.id)

							if len(bernu_mas) == 1:
								kvalitate = vardnica[
								    bernu_mas[0]]  # ja ir tikai viens pēctecis

							else:
								kvalitate1 = vardnica[
								    bernu_mas[0]]  # ja ir divi pēcteci. jāpārbauda
								kvalitate2 = vardnica[bernu_mas[1]]
								# izvēlamies vienu kvalitāti

								if virsotne.limenis % 2 != 0:  #  max level
									kvalitate = kvalitate1 if kvalitate1 >= kvalitate2 else kvalitate2
								else:  #    min level
									kvalitate = kvalitate1 if kvalitate1 <= kvalitate2 else kvalitate2

						vardnica[virsotne.id] = kvalitate

				limenis -= 1  # notiek viss ciklā, ejot pa līmeniem, no lēja uz augšu

			tekosa_virs_nov = vardnica.get(Virsotne.id)
			left_ch_nov = vardnica.get(
			    bernu_masivs[0])  # bernu kvalitātes/ novertējumi
			right_ch_nov = vardnica.get(bernu_masivs[1])

			left_ch = spk.virsotnu_kopa[int(bernu_masivs[0][1:])]
			right_ch = spk.virsotnu_kopa[int(bernu_masivs[1][1:])]

			if left_ch_nov is not None and right_ch_nov is not None:
				if speletajs == 1:  #speletajs ir dators
					if left_ch_nov >= right_ch_nov:
						return left_ch
					else:
						return right_ch

				if speletajs == 2:  #speletajs ir cilvēks
					if left_ch_nov <= right_ch_nov:
						return left_ch
					else:
						return right_ch
				else:
					print("Error")


#Atgriež strupceļa virsotnes.
def get_strupvirs(spk):
	mas = []
	for i in range(len(spk.virsotnu_kopa)):
		if spk.virsotnu_kopa[i].limenis == app.maxlim + 1:
			mas.append(spk.virsotnu_kopa[i])
	return mas


#Pārbauda, vai spēle ir beigusies.
def is_game_over(virs):
	if virs in app.strupvirs:
		return True
	else:
		return False


#Atgriež heiristisko vērtību virsotnei.
def novertet(state, turn):
	#Atgriež starpību starp datora(p2) un cilvēka (p1) punktiem.
	if turn == 1:
		return state.p2 - state.p1
	else:
		return state.p1 - state.p2


#Atgriež iespējamos gājienus.
def iespej_gaj(state):
	mas = []
	for i in spk.loku_kopa[state.id]:
		for j in range(len(spk.virsotnu_kopa)):
			if spk.virsotnu_kopa[j].id == i:
				mas.append(spk.virsotnu_kopa[j])
	return mas


#Min-max algoritma funkcija ar heiristisko novērtējumu.
def min_max_heiristiska(spk, Virsotne, speletajs):
	vardnica = dict()
	if spk.loku_kopa.get(Virsotne.id) is None:
		print("Ievades kļūda, tāda virsotne neeksistē")
	else:
		bernu_masivs = spk.loku_kopa.get(Virsotne.id)
		if len(bernu_masivs) == 1:
			# ja ir tikai viens gājiens
			return spk.virsotnu_kopa[int(bernu_masivs[0][1:])]
		else:
			i = len(spk.virsotnu_kopa)
			visa_koka_garums = spk.virsotnu_kopa[i - 1].limenis
			virs_lim = Virsotne.limenis
			if virs_lim + 3 <= visa_koka_garums:
				max_limenis = virs_lim + 3
			else:
				max_limenis = visa_koka_garums

			max_limenis = max_limenis + 1
			limenis = max_limenis
			kvalitate = 0
			while limenis >= Virsotne.limenis:
				for virsotne in spk.virsotnu_kopa:
					if virsotne.limenis == limenis:

						if virsotne.limenis == max_limenis or spk.loku_kopa.get(
						    virsotne.id) == None:
							kvalitate = virsotne.p1 - virsotne.p2  # heiristiska funkcija
							#print(virsotne.id)
						elif virsotne.limenis < max_limenis:
							#print(virsotne.id)
							bernu_mas = spk.loku_kopa.get(virsotne.id)
							if len(bernu_mas) == 1:
								# ja ir tikai viens pēctecis
								kvalitate = vardnica[bernu_mas[0]]
							else:
								# ja ir divi pēcteci;
								kvalitate1 = vardnica[bernu_mas[0]]
								kvalitate2 = vardnica[bernu_mas[1]]
								# izvēlamies vienu kvalitāti
								if virsotne.limenis % 2 != 0:  #  max level
									kvalitate = kvalitate1 if kvalitate1 >= kvalitate2 else kvalitate2
								else:  #    min level
									kvalitate = kvalitate1 if kvalitate1 <= kvalitate2 else kvalitate2

						vardnica[virsotne.id] = kvalitate

				limenis -= 1  # notiek viss ciklā, ejot pa līmeniem no lēja uz augšu

			tekosa_virs_nov = vardnica.get(Virsotne.id)
			# bernu kvalitātes/ novertējumi
			left_ch_nov = vardnica.get(bernu_masivs[0])
			right_ch_nov = vardnica.get(bernu_masivs[1])

			left_ch = spk.virsotnu_kopa[int(bernu_masivs[0][1:])]
			right_ch = spk.virsotnu_kopa[int(bernu_masivs[1][1:])]

			if left_ch_nov is not None and right_ch_nov is not None:
				if speletajs == 1:  #speletajs ir dators
					if left_ch_nov >= right_ch_nov:
						return left_ch
					else:
						return right_ch
				if speletajs == 2:  #speletajs ir cilvēks
					if left_ch_nov <= right_ch_nov:
						return left_ch
					else:
						return right_ch
				else:
					print("Error")


#Alfa-beta algoritma funkcija
def alpha_beta(state, depth, alpha, beta, playermove, turn):
	if depth == 0 or is_game_over(state):
		return novertet(state, turn)

	if turn == 1:
		if playermove:
			max_eval = -math.inf
			for child_state in iespej_gaj(state):
				eval = alpha_beta(child_state, depth - 1, alpha, beta, False, turn)
				#print(child_state.id)
				max_eval = max(max_eval, eval)
				alpha = max(alpha, eval)
				if beta <= alpha:
					break
			return max_eval

		else:
			min_eval = math.inf
			for child_state in iespej_gaj(state):
				eval = alpha_beta(child_state, depth - 1, alpha, beta, True, turn)
				#print(child_state.id)
				min_eval = min(min_eval, eval)
				beta = min(beta, eval)
				if beta <= alpha:
					break
			return min_eval

	if turn == 2:
		if not playermove:
			max_eval = -math.inf
			for child_state in iespej_gaj(state):
				#print(child_state.id)
				eval = alpha_beta(child_state, depth - 1, alpha, beta, True, turn)
				max_eval = max(max_eval, eval)
				alpha = max(alpha, eval)
				if beta <= alpha:
					break
			return max_eval

		else:
			min_eval = math.inf
			for child_state in iespej_gaj(state):
				#print(child_state.id)
				eval = alpha_beta(child_state, depth - 1, alpha, beta, False, turn)
				min_eval = min(min_eval, eval)
				beta = min(beta, eval)
				if beta <= alpha:
					break
			return min_eval
	return 0


#Funkcija, kas nosaka labāko gājienu.
def labakais_gaj(virsot, depth, speletajs, turn):
	best_eval = -math.inf
	best_move = Virsotne('A0', root, 0, 0, 0, 1)
	for child_virsot in iespej_gaj(virsot):
		eval = alpha_beta(child_virsot, depth - 1, -math.inf, math.inf, speletajs,
		                  turn)
		if eval > best_eval:
			best_eval = eval
			best_move = child_virsot
	return best_move


#Klase, kas atbilst vienai virsotnei spēles kokā
class Virsotne:

	def __init__(self, id, virkne, p1, p2, bank, limenis):
		self.id = id
		self.virkne = virkne
		self.p1 = p1
		self.p2 = p2
		self.bank = bank
		self.limenis = limenis


#Klase, kas atbilst spēles kokam
class Speles_koks:

	def __init__(self):
		self.virsotnu_kopa = []
		self.loku_kopa = dict()
		self.childloku_kopa = dict()

	#Klases Speles_koks metode, kas pievieno spēles kokam jaunu virsotni, kuru saņem kā argumentu.
	def pievienot_virsotni(self, Virsotne):
		self.virsotnu_kopa.append(Virsotne)

	#Klases Speles_koks metode, kura papildina loku kopu, saņemot kā argumentus
	#virsotnes identifikatoru, no kuras loks iziet, un virsotnes identifikatoru, kurā loks ieiet.
	def pievienot_loku(self, sakumvirsotne_id, beiguvirsotne_id):
		self.loku_kopa[sakumvirsotne_id] = self.loku_kopa.get(
		    sakumvirsotne_id, []) + [beiguvirsotne_id]

	def pievienot_childloku(self, sakumvirsotne_id, beiguvirsotne_id):
		self.childloku_kopa[sakumvirsotne_id] = self.childloku_kopa.get(
		    sakumvirsotne_id, []) + [beiguvirsotne_id]


#Klase, kas izveido grafisko izskārni.
class App:
	spk = Speles_koks()
	maxlim = 0
	algor = 1
	firstmove = 1
	playerMove = True
	currentNumber = Virsotne("A0", 20000, 0, 0, 0, 1)
	strupvirs = []
	fullTree = True

	def __init__(self, root):
		#Uzstāda virsrakstu.
		root.title("Divide Game")
		#Uzstāda loga izmērus.
		width = 800
		height = 600
		screenwidth = root.winfo_screenwidth()
		screenheight = root.winfo_screenheight()
		alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
		                            (screenheight - height) / 2)
		root.geometry(alignstr)
		root.resizable(width=False, height=False)

		topLabel = tk.Label(root)
		topLabel["bg"] = "#9565e7"
		topLabel["cursor"] = "circle"
		topLabel["disabledforeground"] = "#a92626"
		ft = tkFont.Font(family='Times', size=22)
		topLabel["font"] = ft
		topLabel["fg"] = "#ffffff"
		topLabel["justify"] = "center"
		topLabel["text"] = "Divide game"
		topLabel["relief"] = "groove"
		topLabel.place(x=0, y=30, width=800, height=80)

		bottomLabel = tk.Label(root)
		bottomLabel["bg"] = "#9565e7"
		ft = tkFont.Font(family='Times', size=10)
		bottomLabel["font"] = ft
		bottomLabel["fg"] = "#333333"
		bottomLabel["justify"] = "center"
		bottomLabel["text"] = ""
		bottomLabel.place(x=0, y=480, width=800, height=80)

		self.algorithmLabel = tk.Label(root)
		self.algorithmLabel["bg"] = "#5fb878"
		ft = tkFont.Font(family='Times', size=18)
		self.algorithmLabel["font"] = ft
		self.algorithmLabel["fg"] = "#333333"
		self.algorithmLabel["justify"] = "center"
		self.algorithmLabel["text"] = "Algorithm"
		self.algorithmLabel.place(x=150, y=130, width=500, height=40)

		self.typeLabel = tk.Label(root)
		self.typeLabel["bg"] = "#5fb878"
		ft = tkFont.Font(family='Times', size=18)
		self.typeLabel["font"] = ft
		self.typeLabel["fg"] = "#333333"
		self.typeLabel["justify"] = "center"
		self.typeLabel["text"] = "Type"
		self.typeLabel.place(x=150, y=350, width=500, height=40)

		self.UseFullTree = tk.Button(root)
		self.UseFullTree["bg"] = "#f0f0f0"
		ft = tkFont.Font(family='Times', size=10)
		self.UseFullTree["font"] = ft
		self.UseFullTree["fg"] = "#000000"
		self.UseFullTree["justify"] = "center"
		self.UseFullTree["text"] = "Use full tree"
		self.UseFullTree.place(x=170, y=400, width=225, height=35)
		self.UseFullTree["command"] = self.UseFullTree_command

		self.UseHeiristicFunction = tk.Button(root)
		self.UseHeiristicFunction["bg"] = "#f0f0f0"
		ft = tkFont.Font(family='Times', size=10)
		self.UseHeiristicFunction["font"] = ft
		self.UseHeiristicFunction["fg"] = "#000000"
		self.UseHeiristicFunction["justify"] = "center"
		self.UseHeiristicFunction["text"] = "Use Heuristic Function"
		self.UseHeiristicFunction.place(x=410, y=400, width=225, height=35)
		self.UseHeiristicFunction["command"] = self.UseHeiristicFunction_command

		self.MinMaxButton = tk.Button(root)
		self.MinMaxButton["bg"] = "#f0f0f0"
		ft = tkFont.Font(family='Times', size=10)
		self.MinMaxButton["font"] = ft
		self.MinMaxButton["fg"] = "#000000"
		self.MinMaxButton["justify"] = "center"
		self.MinMaxButton["text"] = "MinMax"
		self.MinMaxButton.place(x=170, y=180, width=225, height=35)
		self.MinMaxButton["command"] = self.MinMaxButton_command

		self.AlphaBetaButton = tk.Button(root)
		self.AlphaBetaButton["bg"] = "#f0f0f0"
		ft = tkFont.Font(family='Times', size=10)
		self.AlphaBetaButton["font"] = ft
		self.AlphaBetaButton["fg"] = "#000000"
		self.AlphaBetaButton["justify"] = "center"
		self.AlphaBetaButton["text"] = "AlphaBeta"
		self.AlphaBetaButton.place(x=410, y=180, width=225, height=35)
		self.AlphaBetaButton["command"] = self.AlphaBetaButton_command

		self.FirstTurnLabel = tk.Label(root)
		self.FirstTurnLabel["bg"] = "#5fb878"
		ft = tkFont.Font(family='Times', size=18)
		self.FirstTurnLabel["font"] = ft
		self.FirstTurnLabel["fg"] = "#333333"
		self.FirstTurnLabel["justify"] = "center"
		self.FirstTurnLabel["text"] = "First Turn"
		self.FirstTurnLabel.place(x=150, y=240, width=500, height=40)

		self.PlayerButton = tk.Button(root)
		self.PlayerButton["bg"] = "#f0f0f0"
		ft = tkFont.Font(family='Times', size=10)
		self.PlayerButton["font"] = ft
		self.PlayerButton["fg"] = "#000000"
		self.PlayerButton["justify"] = "center"
		self.PlayerButton["text"] = "Player"
		self.PlayerButton.place(x=170, y=290, width=225, height=35)
		self.PlayerButton["command"] = self.PlayerButton_command

		self.ComputerButton = tk.Button(root)
		self.ComputerButton["bg"] = "#f0f0f0"
		ft = tkFont.Font(family='Times', size=10)
		self.ComputerButton["font"] = ft
		self.ComputerButton["fg"] = "#000000"
		self.ComputerButton["justify"] = "center"
		self.ComputerButton["text"] = "Computer"
		self.ComputerButton.place(x=410, y=290, width=225, height=35)
		self.ComputerButton["command"] = self.ComputerButton_command

		self.startButton = tk.Button(root)
		self.startButton["bg"] = "#1e9fff"
		ft = tkFont.Font(family='Times', size=18)
		self.startButton["font"] = ft
		self.startButton["fg"] = "#ffffff"
		self.startButton["justify"] = "center"
		self.startButton["text"] = "Start"
		self.startButton.place(x=330, y=490, width=145, height=52)
		self.startButton["command"] = self.StartButton

	def CreateChoiseButtons(self, root, first, second, third, fourth, fifth):
		self.FirstNumberButton = tk.Button(root)
		self.FirstNumberButton["bg"] = "#f0f0f0"
		self.ft = tkFont.Font(family='Times', size=10)
		self.FirstNumberButton["font"] = self.ft
		self.FirstNumberButton["fg"] = "#000000"
		self.FirstNumberButton["justify"] = "center"
		self.FirstNumberButton["text"] = first
		self.FirstNumberButton.place(x=40, y=150, width=115, height=45)
		self.FirstNumberButton["command"] = lambda: self.ChooseNumber(first)

		self.SecondNumberButton = tk.Button(root)
		self.SecondNumberButton["bg"] = "#f0f0f0"
		self.ft = tkFont.Font(family='Times', size=10)
		self.SecondNumberButton["font"] = self.ft
		self.SecondNumberButton["fg"] = "#000000"
		self.SecondNumberButton["justify"] = "center"
		self.SecondNumberButton["text"] = second
		self.SecondNumberButton.place(x=190, y=150, width=115, height=45)
		self.SecondNumberButton["command"] = lambda: self.ChooseNumber(second)

		self.ThirdNumberButton = tk.Button(root)
		self.ThirdNumberButton["bg"] = "#f0f0f0"
		self.ft = tkFont.Font(family='Times', size=10)
		self.ThirdNumberButton["font"] = self.ft
		self.ThirdNumberButton["fg"] = "#000000"
		self.ThirdNumberButton["justify"] = "center"
		self.ThirdNumberButton["text"] = third
		self.ThirdNumberButton.place(x=340, y=150, width=115, height=45)
		self.ThirdNumberButton["command"] = lambda: self.ChooseNumber(third)

		self.FourthNumberButton = tk.Button(root)
		self.FourthNumberButton["bg"] = "#f0f0f0"
		self.ft = tkFont.Font(family='Times', size=10)
		self.FourthNumberButton["font"] = self.ft
		self.FourthNumberButton["fg"] = "#000000"
		self.FourthNumberButton["justify"] = "center"
		self.FourthNumberButton["text"] = fourth
		self.FourthNumberButton.place(x=490, y=150, width=115, height=45)
		self.FourthNumberButton["command"] = lambda: self.ChooseNumber(fourth)

		self.FifthNumberButton = tk.Button(root)
		self.FifthNumberButton["bg"] = "#f0f0f0"
		self.ft = tkFont.Font(family='Times', size=10)
		self.FifthNumberButton["font"] = self.ft
		self.FifthNumberButton["fg"] = "#000000"
		self.FifthNumberButton["justify"] = "center"
		self.FifthNumberButton["text"] = fifth
		self.FifthNumberButton.place(x=640, y=150, width=115, height=45)
		self.FifthNumberButton["command"] = lambda: self.ChooseNumber(fifth)

	def StartButton(self):
		temp_root = generate_root()
		self.CreateChoiseButtons(root, temp_root[0], temp_root[1], temp_root[2],
		                         temp_root[3], temp_root[4])
		self.startButton.destroy()
		self.AlphaBetaButton.destroy()
		self.MinMaxButton.destroy()
		self.algorithmLabel.destroy()
		self.FirstTurnLabel.destroy()
		self.PlayerButton.destroy()
		self.ComputerButton.destroy()
		self.UseFullTree.destroy()
		self.UseHeiristicFunction.destroy()
		self.typeLabel.destroy()

	def ChooseNumber(self, number):
		self.FirstNumberButton.destroy()
		self.SecondNumberButton.destroy()
		self.ThirdNumberButton.destroy()
		self.FourthNumberButton.destroy()
		self.FifthNumberButton.destroy()
		self.spk = generate_tree(number)
		self.currentNumber = self.spk.virsotnu_kopa[0]
		self.GameNumber = tk.Label(root)
		self.GameNumber["bg"] = "#90f090"
		ft = tkFont.Font(family='Times', size=22)
		self.GameNumber["font"] = ft
		self.GameNumber["fg"] = "#000000"
		self.GameNumber["justify"] = "center"
		self.GameNumber["text"] = number
		self.GameNumber.place(x=320, y=150, width=150, height=75)

		labelNumber = tk.Label(root)
		ft = tkFont.Font(family='Times', size=10)
		labelNumber["font"] = ft
		labelNumber["fg"] = "#333333"
		labelNumber["justify"] = "center"
		labelNumber["text"] = "Number:"
		labelNumber.place(x=345, y=120, width=100, height=30)

		self.PlayerScore = tk.Label(root)
		ft = tkFont.Font(family='Times', size=22)
		self.PlayerScore["font"] = ft
		self.PlayerScore["fg"] = "#333333"
		self.PlayerScore["justify"] = "center"
		self.PlayerScore["text"] = "0"
		self.PlayerScore.place(x=170, y=150, width=140, height=70)

		self.ComputerScore = tk.Label(root)
		ft = tkFont.Font(family='Times', size=22)
		self.ComputerScore["font"] = ft
		self.ComputerScore["fg"] = "#333333"
		self.ComputerScore["justify"] = "center"
		self.ComputerScore["text"] = "0"
		self.ComputerScore.place(x=480, y=150, width=140, height=70)

		labelPlayerScoreText = tk.Label(root)
		ft = tkFont.Font(family='Times', size=10)
		labelPlayerScoreText["font"] = ft
		labelPlayerScoreText["fg"] = "#333333"
		labelPlayerScoreText["justify"] = "center"
		labelPlayerScoreText["text"] = "Player score"
		labelPlayerScoreText.place(x=195, y=120, width=90, height=30)

		labelBankScoreText = tk.Label(root)
		ft = tkFont.Font(family='Times', size=10)
		labelBankScoreText["font"] = ft
		labelBankScoreText["fg"] = "#333333"
		labelBankScoreText["justify"] = "center"
		labelBankScoreText["text"] = "Bank"
		labelBankScoreText.place(x=195, y=240, width=90, height=30)

		self.BankScore = tk.Label(root)
		ft = tkFont.Font(family='Times', size=22)
		self.BankScore["font"] = ft
		self.BankScore["fg"] = "#333333"
		self.BankScore["justify"] = "center"
		self.BankScore["text"] = "0"
		self.BankScore.place(x=170, y=270, width=140, height=70)

		labelComputerScoreText = tk.Label(root)
		ft = tkFont.Font(family='Times', size=10)
		labelComputerScoreText["font"] = ft
		labelComputerScoreText["fg"] = "#333333"
		labelComputerScoreText["justify"] = "center"
		labelComputerScoreText["text"] = "Computer score"
		labelComputerScoreText.place(x=505, y=120, width=90, height=30)

		self.DivideByTwoButton = tk.Button(root)
		self.DivideByTwoButton["bg"] = "#f0f0f0"
		ft = tkFont.Font(family='Times', size=18)
		self.DivideByTwoButton["font"] = ft
		self.DivideByTwoButton["fg"] = "#000000"
		self.DivideByTwoButton["justify"] = "center"
		self.DivideByTwoButton["text"] = "÷2"
		self.DivideByTwoButton.place(x=320, y=260, width=60, height=60)
		self.DivideByTwoButton["command"] = self.DivideByTwo

		self.DivideByThreeButton = tk.Button(root)
		self.DivideByThreeButton["bg"] = "#f0f0f0"
		ft = tkFont.Font(family='Times', size=18)
		self.DivideByThreeButton["font"] = ft
		self.DivideByThreeButton["fg"] = "#000000"
		self.DivideByThreeButton["justify"] = "center"
		self.DivideByThreeButton["text"] = "÷3"
		self.DivideByThreeButton.place(x=410, y=260, width=60, height=60)
		self.DivideByThreeButton["command"] = self.DivideByThree

		self.AskButton = tk.Button(root)
		self.AskButton["bg"] = "#f0f0f0"
		ft = tkFont.Font(family='Times', size=10)
		self.AskButton["font"] = ft
		self.AskButton["fg"] = "#000000"
		self.AskButton["justify"] = "center"
		self.AskButton["text"] = "Ask Computer To Move"
		self.AskButton.place(x=320, y=340, width=151, height=67)
		self.AskButton["command"] = self.AskComputer

		self.WinLabel = tk.Label(root)
		self.WinLabel["bg"] = "#9565e7"
		ft = tkFont.Font(family='Times', size=28)
		self.WinLabel["font"] = ft
		self.WinLabel["fg"] = "#ffffff"
		self.WinLabel["justify"] = "center"
		self.WinLabel["text"] = ""
		self.WinLabel.place(x=250, y=490, width=300, height=60)

		if self.firstmove == 1:
			self.DivideByTwoButton["state"] = "active"
			self.DivideByThreeButton["state"] = "active"
			self.AskButton["state"] = "disabled"
		if self.firstmove == 2:
			self.DivideByTwoButton["state"] = "disabled"
			self.DivideByThreeButton["state"] = "disabled"
			self.AskButton["state"] = "active"

	def CheckLooseCondition(self):
		if self.currentNumber in app.strupvirs:
			if self.firstmove == 1:
				if self.currentNumber.p1 > self.currentNumber.p2:
					self.WinLabel["text"] = "Player Wins!"
				if self.currentNumber.p1 < self.currentNumber.p2:
					self.WinLabel["text"] = "Computer Wins!"
				if self.currentNumber.p1 == self.currentNumber.p2:
					self.WinLabel["text"] = "Draw!"
			if self.firstmove == 2:
				if self.currentNumber.p1 < self.currentNumber.p2:
					self.WinLabel["text"] = "Player Wins!"
				if self.currentNumber.p1 > self.currentNumber.p2:
					self.WinLabel["text"] = "Computer Wins!"
				if self.currentNumber.p1 == self.currentNumber.p2:
					self.WinLabel["text"] = "Draw!"
			self.AskButton["state"] = "disabled"
			self.DivideByTwoButton["state"] = "disabled"
			self.DivideByThreeButton["state"] = "disabled"

			self.restartButton = tk.Button(root)
			self.restartButton["bg"] = "#1e9fff"
			ft = tkFont.Font(family='Times', size=18)
			self.restartButton["font"] = ft
			self.restartButton["fg"] = "#ffffff"
			self.restartButton["justify"] = "center"
			self.restartButton["text"] = "Restart"
			self.restartButton.place(x=325, y=420, width=145, height=52)
			self.restartButton["command"] = RestartGame

	def MinMaxButton_command(self):
		self.MinMaxButton["bg"] = "#1e9fff"
		self.AlphaBetaButton["bg"] = "#ffffff"
		self.algor = 1

	def AlphaBetaButton_command(self):
		self.MinMaxButton["bg"] = "#ffffff"
		self.AlphaBetaButton["bg"] = "#1e9fff"
		self.algor = 2

	def PlayerButton_command(self):
		self.PlayerButton["bg"] = "#1e9fff"
		self.ComputerButton["bg"] = "#ffffff"
		self.firstmove = 1
		self.playerMove = True

	def ComputerButton_command(self):
		self.PlayerButton["bg"] = "#ffffff"
		self.ComputerButton["bg"] = "#1e9fff"
		self.firstmove = 2
		self.playerMove = False

	def UseFullTree_command(self):
		self.UseFullTree["bg"] = "#1e9fff"
		self.UseHeiristicFunction["bg"] = "#ffffff"
		self.fullTree = True

	def UseHeiristicFunction_command(self):
		self.UseFullTree["bg"] = "#ffffff"
		self.UseHeiristicFunction["bg"] = "#1e9fff"
		self.fullTree = False

	#f-ja kuru izsauc poga ÷2
	def DivideByTwo(self):
		n = 2
		if self.currentNumber.virkne % 2 == 0:
			for i in range(len(spk.virsotnu_kopa)):
				if spk.virsotnu_kopa[i].virkne == self.currentNumber.virkne // n:
					if self.currentNumber.id in spk.loku_kopa and len(
					    spk.loku_kopa[self.currentNumber.id]) == 2:
						if spk.virsotnu_kopa[i].id == spk.loku_kopa[self.currentNumber.id][
						    0] or spk.virsotnu_kopa[i].id == spk.loku_kopa[
						        self.currentNumber.id][1]:
							self.currentNumber = spk.virsotnu_kopa[i]
							break
					if self.currentNumber.id in spk.loku_kopa and len(
					    spk.loku_kopa[self.currentNumber.id]) == 1:
						if spk.virsotnu_kopa[i].id == spk.loku_kopa[
						    self.currentNumber.id][0]:
							self.currentNumber = spk.virsotnu_kopa[i]
							break

		if self.firstmove == 1:
			self.PlayerScore["text"] = self.currentNumber.p1
			self.ComputerScore["text"] = self.currentNumber.p2
		else:
			self.PlayerScore["text"] = self.currentNumber.p2
			self.ComputerScore["text"] = self.currentNumber.p1
		self.BankScore["text"] = self.currentNumber.bank
		self.GameNumber["text"] = self.currentNumber.virkne
		self.DivideByThreeButton["state"] = "disabled"
		self.DivideByTwoButton["state"] = "disabled"
		self.AskButton["state"] = "active"
		self.playerMove = not self.playerMove

		self.CheckLooseCondition()

	#f-ja kuru izsauc poga ÷3
	def DivideByThree(self):
		n = 3
		if self.currentNumber.virkne % 3 == 0:
			for i in range(len(spk.virsotnu_kopa)):
				if spk.virsotnu_kopa[i].virkne == self.currentNumber.virkne // n:
					if self.currentNumber.id in spk.loku_kopa and len(
					    spk.loku_kopa[self.currentNumber.id]) == 2:
						if spk.virsotnu_kopa[i].id == spk.loku_kopa[self.currentNumber.id][
						    0] or spk.virsotnu_kopa[i].id == spk.loku_kopa[
						        self.currentNumber.id][1]:
							self.currentNumber = spk.virsotnu_kopa[i]
							break
					if self.currentNumber.id in spk.loku_kopa and len(
					    spk.loku_kopa[self.currentNumber.id]) == 1:
						if spk.virsotnu_kopa[i].id == spk.loku_kopa[
						    self.currentNumber.id][0]:
							self.currentNumber = spk.virsotnu_kopa[i]
							break
		if self.firstmove == 1:
			self.PlayerScore["text"] = self.currentNumber.p1
			self.ComputerScore["text"] = self.currentNumber.p2
		else:
			self.PlayerScore["text"] = self.currentNumber.p2
			self.ComputerScore["text"] = self.currentNumber.p1
		self.GameNumber["text"] = self.currentNumber.virkne
		self.DivideByThreeButton["state"] = "disabled"
		self.DivideByTwoButton["state"] = "disabled"
		self.AskButton["state"] = "active"
		self.playerMove = not self.playerMove
		self.BankScore["text"] = self.currentNumber.bank
		self.CheckLooseCondition()

	def AskComputer(self):
		if self.algor == 1:
			if self.fullTree == True:
				if self.firstmove == 1:
					#t0 = time.time()
					self.currentNumber = min_max(self.spk, self.currentNumber, 2)
					#t1 = time.time()
					#print("Time of MinMax", t1 - t0)
				else:
					#t0 = time.time()
					self.currentNumber = min_max(self.spk, self.currentNumber, 1)
					#t1 = time.time()
					#print("Time of MinMax", t1 - t0)

			else:
				if self.firstmove == 1:
					#t0 = time.time()
					self.currentNumber = min_max_heiristiska(self.spk,
					                                         self.currentNumber, 2)
					#t1 = time.time()
					#print("Time of MinMax Heuristic", t1 - t0)
				else:
					#t0 = time.time()
					self.currentNumber = min_max_heiristiska(self.spk,
					                                         self.currentNumber, 1)
					#t1 = time.time()
					#print("Time of MinMax Heuristic", t1 - t0)

		if self.algor == 2:
			if self.fullTree == True:
				#t0 = time.time()
				self.currentNumber = labakais_gaj(self.currentNumber, self.maxlim + 1,
				                                  self.playerMove, self.firstmove)
				#t1 = time.time()
				#print("Time of AlphaBeta", t1 - t0)
			else:
				if self.maxlim + 1 > 3:
					#t0 = time.time()
					self.currentNumber = labakais_gaj(self.currentNumber, 3,
					                                  self.playerMove, self.firstmove)
					#t1 = time.time()
					#print("Time of AlphaBeta Heuristic", t1 - t0)
				else:
					#t0 = time.time()
					self.currentNumber = labakais_gaj(self.currentNumber,
					                                  self.maxlim + 1, self.playerMove,
					                                  self.firstmove)
					#t1 = time.time()
					#print("Time of AlphaBeta Heuristic", t1 - t0)

		if self.currentNumber.virkne % 3 != 0:
			self.DivideByThreeButton["state"] = "disabled"
		else:
			self.DivideByThreeButton["state"] = "active"

		if self.currentNumber.virkne % 2 != 0:
			self.DivideByTwoButton["state"] = "disabled"
		else:
			self.DivideByTwoButton["state"] = "active"

		if self.firstmove == 1:
			self.PlayerScore["text"] = self.currentNumber.p1
			self.ComputerScore["text"] = self.currentNumber.p2
		else:
			self.PlayerScore["text"] = self.currentNumber.p2
			self.ComputerScore["text"] = self.currentNumber.p1

		self.AskButton["state"] = "disabled"
		self.playerMove = not self.playerMove
		self.GameNumber["text"] = self.currentNumber.virkne
		self.BankScore["text"] = self.currentNumber.bank
		self.CheckLooseCondition()


#Galvenais bloks, kas izveido logu.
if __name__ == "__main__":
	spk = Speles_koks()
	root = tk.Tk()
	app = App(root)
	root.mainloop()
