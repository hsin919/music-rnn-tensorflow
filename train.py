from data_util import SeqData
from model import Model
from params import *

import tensorflow as tf
from tensorflow.models.rnn import rnn, rnn_cell
import numpy as np

'''
LSTM RNN For Predicting the Next Vector Element in a Sequence 
'''

# Parameters
params = get_params()
training_iters = 30000
display_step = 10

print('Creating Data...')
data = SeqData(params)

print('Building Model...')
model = Model(params)

# Initializing the variables
init = tf.initialize_all_variables()

# Saver
saver = tf.train.Saver()

def istate():
	return np.zeros((params['batch_size'], 2*params['n_hidden']))

# Launch the graph
with tf.Session() as sess:
	sess.run(init)
	step = 1
	while step * params['batch_size'] < training_iters:

		# Fit training using batch data
		batch_xs, batch_ys = data.next_train()
		feed_dict = {model.x: batch_xs, model.y: batch_ys, model.initial: istate() }
		sess.run(model.opt, feed_dict=feed_dict)

		if step % display_step == 0:
			# Calculate batch accuracy
			feed_dict = {model.x: batch_xs, model.y: batch_ys, model.initial: istate() }
			acc = sess.run(model.acc, feed_dict=feed_dict)

			# Calculate batch loss
			feed_dict = {model.x: batch_xs, model.y: batch_ys, model.initial: istate() }
			loss = sess.run(model.cost, feed_dict=feed_dict)
			print ("Iter " + str(step*params['batch_size']) + 
					", Minibatch Loss= " + "{:.6f}".format(loss) + \
					", Training Accuracy= " + "{:.5f}".format(acc))
		step += 1
	print "Optimization Finished!"

	test_x,test_y = data.next_test()
	feed_dict = {model.x: test_x, model.y: test_y, model.initial: istate() }
	test_acc = sess.run(model.acc, feed_dict=feed_dict)
	print "Testing Accuracy:", test_acc

	saver.save(sess, "save/model.ckpt")