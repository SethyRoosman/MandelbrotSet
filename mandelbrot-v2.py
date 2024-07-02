from __future__ import division
from multiprocessing import Pool
import plotly.graph_objects as go
import plotly.express as px
import pandas
import numpy as np
import cv2 as cv
import os
import time
import math

"""
My plan with this new updated mandelbrot thing is efficiency
"""

# Image size (pixels)
WIDTH = 1440
HEIGHT = 900

NO_IMG = True
SAVE_IMG = True
MAKE_VID = True

# Make Plot.ly graph of performance?

# Plot window

ptx = -1.7693831791955150182138472860854737829057472636547514374655282165278881912647564588361634463895296673044858257818203031574874912384217194031282461951137475212550848062085787454772803303225167998662391124184542743017129214423639793169296754394181656831301342622793541423768572435783910849972056869527305207508191441734781061794290699753174911133714351734166117456520272756159178932042908932465102671790878414664628213755990650460738372283470777870306458882898202604001744348908388844962887074505853707095832039410323454920540534378406083202543002080240776000604510883136400112955848408048692373051275999457470473671317598770623174665886582323619043055508383245744667325990917947929662025877792679499645660786033978548337553694613673529685268652251959453874971983533677423356377699336623705491817104771909424891461757868378026419765129606526769522898056684520572284028039883286225342392455089357242793475261134567912757009627599451744942893765395578578179137375672787942139328379364197492987307203001409779081030965660422490200242892023288520510396495370720268688377880981691988243756770625044756604957687314689241825216171368155083773536285069411856763404065046728379696513318216144607821920824027797857625921782413101273331959639628043420017995090636222818019324038366814798438238540927811909247543259203596399903790614916969910733455656494065224399357601105072841234072044886928478250600986666987837467585182504661923879353345164721140166670708133939341595205900643816399988710049682525423837465035288755437535332464750001934325685009025423642056347757530380946799290663403877442547063918905505118152350633031870270153292586262005851702999524577716844595335385805548908126325397736860678083754587744508953038826602270140731059161305854135393230132058326419325267890909463907657787245924319849651660028931472549400310808097453589135197164989941931054546261747594558823583006437970585216728326439804654662779987947232731036794099604937358361568561860539962449610052967074013449293876425609214167615079422980743121960127425155223407999875999884
pty = 0.00423684791873677221492650717136799707668267091740375727945943565011234400080554515730243099502363650631353268335965257182300494805538736306127524814939292355930892834392050796724887904921986666045576626946900666103494014904714323725586979789908520656683202658064024115300378826789786394641622035341055102900456305723718684527210377325846307917512628774672005693326232806953822796755832517188873479124361430989485495501124096329421682827330693532171505367455526637382706988583456915684673202462211937384523487065290004627037270912806345336469007546411109669407622004367957958476890043040953462048335322273359167297049252960438077167010004209439515213189081508634843224000870136889065895088138204552309352430462782158649681507477960551795646930149740918234645225076516652086716320503880420325704104486903747569874284714830068830518642293591138468762031036739665945023607640585036218668993884533558262144356760232561099772965480869237201581493393664645179292489229735815054564819560512372223360478737722905493126886183195223860999679112529868068569066269441982065315045621648665342365985555395338571505660132833205426100878993922388367450899066133115360740011553934369094891871075717765803345451791394082587084902236263067329239601457074910340800624575627557843183429032397590197231701822237810014080715216554518295907984283453243435079846068568753674073705720148851912173075170531293303461334037951893251390031841730968751744420455098473808572196768667200405919237414872570568499964117282073597147065847005207507464373602310697663458722994227826891841411512573589860255142210602837087031792012000966856067648730369466249241454455795058209627003734747970517231654418272974375968391462696901395430614200747446035851467531667672250261488790789606038203516466311672579186528473826173569678887596534006782882871835938615860588356076208162301201143845805878804278970005959539875585918686455482194364808816650829446335905975254727342258614604501418057192598810476108766922935775177687770187001388743012888530139038318783958771247007926690
# scale 0.1 gives cool results
scale = 0.98


#scaleiter = 0

# Still frame values
#RE_START = -2
#RE_END = 1
#IM_START = -1
#IM_END = 1

def mandelbrot(c, MAX_ITER):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1

    if n == MAX_ITER:
        return MAX_ITER

    return n
    #return n + 1 - math.log(math.log(abs(z), 2))


"""
Old implementation
"""
def mandelbrot_loops(scaleiter, MAX_ITER):
	# print(f"current iteration is {scaleiter} out of {MAX_ITER}")
	img = np.empty((HEIGHT, WIDTH, 3))

	RE_START = ptx - (((scale) ** scaleiter) * 1.6)
	RE_END = ptx + (((scale) ** scaleiter) * 1.6)
	IM_START = pty - (scale) ** scaleiter
	IM_END = pty + (scale) ** scaleiter

	for x in range(0, WIDTH):
	    for y in range(0, HEIGHT):
	        # Convert pixel coordinate to complex number
	        c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
	                    IM_START + (y / HEIGHT) * (IM_END - IM_START))
	        # Compute the number of iterations
	        m = mandelbrot(c, MAX_ITER)
	        # The color depends on the number of iterations
	        hue = 4 * (m % 64) #int(255 * m / 100)
	        saturation = 255
	        value = 255 if m < MAX_ITER else 0
	        # Plot the point
	        img[y][x] = (hue, saturation, value)
	return img

def run_loops(MAX_ITER, out_dir):
	start = time.time()
	plotting_arr = []

	for scaleiter in range(0, iterations):
		# starting time for plotly graph
		start_iter = time.time()

		hsv = mandelbrot_loops(scaleiter, MAX_ITER)
		hsv_conv = hsv.astype(np.uint8)
		bgr = cv.cvtColor(hsv_conv, cv.COLOR_HSV2BGR)
		if not NO_IMG:
			cv.imshow("mandelbrot", bgr)
			cv.waitKey(1)
		if SAVE_IMG:
			cv.imwrite(f"./{out_dir}/out-{scaleiter}.png", bgr)
		MAX_ITER += 5

		# ending time for plotly graph
		end_iter = time.time() - start_iter
		plotting_arr.append(end_iter)

	end = time.time()
	print(f"time to completion for {iterations}: {end - start} using loops (one process)")
	return plotting_arr

"""
does the calculations for quadrant x (+/- 1/2 width) (+/- 1/2 height)
"""
def mandelbrot_multi_proc(quadrant_n_scale):
	quadrant = quadrant_n_scale[0]
	scaleiter = quadrant_n_scale[1][0]
	MAX_ITER = quadrant_n_scale[1][1]

	# check that we can use int()?
	grid_slice = np.empty((int(HEIGHT/2), int(WIDTH/2), 3))

    # quad. 1 -> [0, width / 2), [0, height/2)
	# quad. 2 -> [width/2, width), [0, height/2)
	# quad. 3 -> [0, width / 2), [height/2, height)
	# quad. 3 -> [width/2, width), [height/2, height)
	offset_x = 0
	offset_y = 0
	if quadrant == 1:
		# print("working on quadrant 1")
		pass
		# already 0,0
	elif quadrant == 2:
		# print("working on quadrant 2")
		offset_x = int(WIDTH/2)
	elif quadrant == 3:
		# print("working on quadrant 3")
		offset_y = int(HEIGHT/2)
	elif quadrant == 4:
		# print("working on quadrant 4")
		offset_x = int(WIDTH/2)
		offset_y = int(HEIGHT/2)
	else:
		print("you shouldn't be here :(")

	RE_START = ptx - (((scale) ** scaleiter) * 1.6)
	RE_END = ptx + (((scale) ** scaleiter) * 1.6)
	IM_START = pty - (scale) ** scaleiter
	IM_END = pty + (scale) ** scaleiter

	for x in range(offset_x, int(WIDTH/2) + offset_x):
	    for y in range(offset_y, int(HEIGHT/2) + offset_y):
	        # Convert pixel coordinate to complex number
	        c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
	                    IM_START + (y / HEIGHT) * (IM_END - IM_START))
	        # Compute the number of iterations
	        m = mandelbrot(c, MAX_ITER)
	        # The color depends on the number of iterations
	        hue = 4 * (m % 64) #int(255 * m / 100)
	        saturation = 255
	        value = 255 if m < MAX_ITER else 0
	        # Plot the point
	        grid_slice[y - offset_y][x - offset_x] = (hue, saturation, value)

	# need to return a dictionary value (so we know the quadrant)
	# print(f"finished computation for quadrant {quadrant}")
	return {str(quadrant): grid_slice}

def run_multi_proc(MAX_ITER, out_dir):
	# quad. 1 -> [0, width / 2), [0, height/2)
	# quad. 2 -> [width/2, width), [0, height/2)
	# quad. 3 -> [0, width / 2), [height/2, height)
	# quad. 3 -> [width/2, width), [height/2, height)
	print(f"starting multi. process run with {NUM_OF_PROC} processes")
	start = time.time()

	plotting_arr = []

	for scaleiter in range(0, iterations):
		# starting time for plotly graph
		start_iter = time.time()

		# print(f"on iteration {scaleiter} out of {MAX_ITER}")
		p = Pool(processes=NUM_OF_PROC)
		# data will be of the form [ dict, dict, dict ]
		second_arg = [scaleiter, MAX_ITER]
		data = p.map(mandelbrot_multi_proc, [[1, second_arg], [2, second_arg], [3, second_arg], [4, second_arg]])
		p.close()
		# concatenate grid slices (quad 1&2, 3&4 -> 1&2 3&4)
		# print(data)

		combined_quads = {}
		for dic_val in data:
			combined_quads.update(dic_val)
		# print(combined_quads)

		out_r1 = np.concatenate((combined_quads["1"], combined_quads["2"]), axis=1)
		out_r2 = np.concatenate((combined_quads["3"], combined_quads["4"]), axis=1)
		out = np.concatenate((out_r1, out_r2), axis=0)

		hsv_conv = out.astype(np.uint8)
		bgr = cv.cvtColor(hsv_conv, cv.COLOR_HSV2BGR)

		if not NO_IMG:
			cv.imshow("mandelbrot", bgr)
			cv.waitKey(1)
		if SAVE_IMG:
			cv.imwrite(f"./{out_dir}/out-{scaleiter}.png", bgr)
		MAX_ITER += 5

		# ending time for plotly graph
		end_iter = time.time() - start_iter
		plotting_arr.append(end_iter)

	end = time.time()
	print(f"time to completion for {iterations}: {end - start} using multi-processing")
	return plotting_arr

# this checks if a directory called "mandelbrot-images-stash" exists
#	if not, it creates the directory and saves the generated images
def img_dir_check(out_dir):
	if not os.path.exists(f"./{out_dir}"):
		os.mkdir(f"./{out_dir}")

# command: ffmpeg -r 60 -f image2 -s 1920x1080 -i pic%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4
# -r is the framerate (fps)
# -crf is the quality, lower means better quality, 15-25 is usually good
# -s is the resolution
# -pix_fmt yuv420p specifies the pixel format, change this as needed
# ^^^ thank you https://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/
def make_vid(out_dir):
	fps = "30"
	res = "1440x900"
	img_form = "out-%d.png"
	args = f"-r {fps} -f image2 -s {res} -i ./{out_dir}/{img_form} -vcodec libx264 -crf 15 -pix_fmt yuv420p "
	# run command f"ffmpeg {args} ./mandelbrot-images-stash/out.mp4"
	os.system(f"ffmpeg {args} ./{out_dir}/out.mp4")
	print("finished making vid.!")

if __name__ == '__main__':
	MAX_ITER = 80
	iterations = 100
	out_dir = "mand2"

	img_dir_check(out_dir)

	NUM_OF_PROC = 4
	proc_4_arr = run_multi_proc(MAX_ITER, out_dir)

	make_vid(out_dir)

	df = pandas.DataFrame(data={"iterations": [i for i in range(0,iterations)]})
	df.insert(1, "4 processes", proc_4_arr)

	colors = px.colors.qualitative.Plotly
	fig = go.Figure()
	fig.update_layout(
		title="Mandelbrot processing time(s)",
		xaxis_title="iterations",
		yaxis_title="computation time (in seconds)",
		legend_title="# of processes",
		)
	fig.add_traces(go.Scatter(x=df["iterations"], y = df['4 processes'], mode = 'lines+markers', line=dict(color=colors[2]), name="4 processes"))
	fig.show()


	# loop_arr = run_loops(MAX_ITER)

	# NUM_OF_PROC = 2
	# proc_2_arr = run_multi_proc(MAX_ITER)

	# NUM_OF_PROC = 4
	# proc_4_arr = run_multi_proc(MAX_ITER)

	# NUM_OF_PROC = 5
	# proc_5_arr = run_multi_proc(MAX_ITER)

	# NUM_OF_PROC = 10
	# proc_10_arr = run_multi_proc(MAX_ITER)

	# df = pandas.DataFrame(data={"iterations": [i for i in range(0,iterations)]})
	# df.insert(1, "for loops", loop_arr)
	# df.insert(2, "2 processes", proc_2_arr)
	# df.insert(3, "4 processes", proc_4_arr)
	# df.insert(4, "5 processes", proc_5_arr)
	# df.insert(5, "10 processes", proc_10_arr)
	# print(df)

	# colors = px.colors.qualitative.Plotly
	# fig = go.Figure()
	# fig.update_layout(
	# 	title="Mandelbrot processing time(s)",
	# 	xaxis_title="iterations",
	# 	yaxis_title="computation time (in seconds)",
	# 	legend_title="# of processes",
	# 	)
	# fig.add_traces(go.Scatter(x=df["iterations"], y = df['for loops'], mode = 'lines+markers', line=dict(color=colors[0]), name="for loops"))
	# fig.add_traces(go.Scatter(x=df["iterations"], y = df['2 processes'], mode = 'lines+markers', line=dict(color=colors[1]), name="2 processes"))
	# fig.add_traces(go.Scatter(x=df["iterations"], y = df['4 processes'], mode = 'lines+markers', line=dict(color=colors[2]), name="4 processes"))
	# fig.add_traces(go.Scatter(x=df["iterations"], y = df['5 processes'], mode = 'lines+markers', line=dict(color=colors[3]), name="5 processes"))
	# fig.add_traces(go.Scatter(x=df["iterations"], y = df['10 processes'], mode = 'lines+markers', line=dict(color=colors[4]), name="10 processes"))
	# fig.show()
