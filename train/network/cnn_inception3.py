import tensorflow as tf
from tensorflow.python.ops import array_ops
import network.networks as networks


INPUT_WIDTH = 299
INPUT_DEPTH = 3

class Inception3(networks.Network):
    
    def __init__(self):
        super().__init__()
        self.conf_steps = 30000
        self.conf_info_per_steps = 50

        self.arg_adam_learning_rate_base = 0.0001
        self.arg_regularization_rate = 0.00004
        self.arg_weights_stddev = 0.1

    def incep_block_a(self, tensor, x_depth, var_pref, name):
        tensor1 = self.lf.Conv_layer(tensor, [1, 64, 1], True, var_pref + "br1_cv1_")
        tensor2 = self.lf.Conv_layer(tensor, [1, 48, 1], True, var_pref + "br2_cv1_")
        tensor2 = self.lf.Conv_layer(tensor2, [5, 64, 1], True, var_pref + "br2_cv2_")
        tensor3 = self.lf.Conv_layer(tensor, [1, 64, 1], True, var_pref + "br3_cv1_")
        tensor3 = self.lf.Conv_layer(tensor3, [3, 96, 1], True, var_pref + "br3_cv2_")
        tensor3 = self.lf.Conv_layer(tensor3, [3, 96, 1], True, var_pref + "br3_cv3_")
        tensor4 = self.lf.Pool_layer(tensor, False, [3, 1], True)
        tensor4 = self.lf.Conv_layer(tensor4, [1, x_depth, 1], True, var_pref + "br4_cv1_")
        return array_ops.concat([tensor1, tensor2, tensor3, tensor4], 3, name = name)

    def incep_block_4(self, tensor):
        tensor1 = self.lf.Conv_layer(tensor, [3, 384, 2], False, "ic4_br1_cv1_")
        tensor2 = self.lf.Conv_layer(tensor, [1, 64, 1], True, "ic4_br2_cv1_")
        tensor2 = self.lf.Conv_layer(tensor2, [3, 96, 1], True, "ic4_br2_cv2_")
        tensor2 = self.lf.Conv_layer(tensor2, [3, 96, 2], False, "ic4_br2_cv3_")
        tensor3 = self.lf.Pool_layer(tensor, True, [3, 2], False)
        return array_ops.concat([tensor1, tensor2, tensor3], 3, name = "incep_block4")

    def incep_block_b(self, tensor, x_depth, var_pref, name):
        tensor1 = self.lf.Conv_layer(tensor, [1, 192, 1], True, var_pref + "br1_cv1_")
        tensor2 = self.lf.Conv_layer(tensor, [1, x_depth, 1], True, var_pref + "br2_cv1_")
        tensor2 = self.lf.Conv_layer(tensor2, [[1, 7], x_depth, 1], True, var_pref + "br2_cv2_")
        tensor2 = self.lf.Conv_layer(tensor2, [[7, 1], 192, 1], True, var_pref + "br2_cv3_")
        tensor3 = self.lf.Conv_layer(tensor, [1, x_depth, 1], True, var_pref + "br3_cv1_")
        tensor3 = self.lf.Conv_layer(tensor3, [[7, 1], x_depth, 1], True, var_pref + "br3_cv2_")
        tensor3 = self.lf.Conv_layer(tensor3, [[1, 7], x_depth, 1], True, var_pref + "br3_cv3_")
        tensor3 = self.lf.Conv_layer(tensor3, [[7, 1], x_depth, 1], True, var_pref + "br3_cv4_")
        tensor3 = self.lf.Conv_layer(tensor3, [[1, 7], 192, 1], True, var_pref + "br3_cv5_")
        tensor4 = self.lf.Pool_layer(tensor, False, [3, 1], True)
        tensor4 = self.lf.Conv_layer(tensor4, [1, 192, 1], True, var_pref + "br4_cv1_")
        return array_ops.concat([tensor1, tensor2, tensor3, tensor4], 3, name = name)

    def incep_block_9(self, tensor):
        tensor1 = self.lf.Conv_layer(tensor, [1, 192, 1], True, "ic9_br1_cv1_")
        tensor1 = self.lf.Conv_layer(tensor1, [3, 320, 2], False, "ic9_br1_cv2_")
        tensor2 = self.lf.Conv_layer(tensor, [1, 192, 1], True, "ic9_br2_cv1_")
        tensor2 = self.lf.Conv_layer(tensor2, [[1, 7], 192, 1], True, "ic9_br2_cv2_")
        tensor2 = self.lf.Conv_layer(tensor2, [[7, 1], 192, 1], True, "ic9_br2_cv3_")
        tensor2 = self.lf.Conv_layer(tensor2, [3, 192, 2], False, "ic9_br2_cv4_")
        tensor3 = self.lf.Pool_layer(tensor, True, [3, 2], False)
        return array_ops.concat([tensor1, tensor2, tensor3], 3, name = "incep_block9")

    def incep_block_c(self, tensor, var_pref, name):
        tensor1 = self.lf.Conv_layer(tensor, [1, 320, 1], True, var_pref + "br1_cv1_")
        tensor2 = self.lf.Conv_layer(tensor, [1, 384, 1], True, var_pref + "br2_cv1_")
        tensor2a = self.lf.Conv_layer(tensor2, [[1, 3], 384, 1], True, var_pref + "br2_cv2a_")
        tensor2b = self.lf.Conv_layer(tensor2, [[3, 1], 384, 1], True, var_pref + "br2_cv2b_")
        tensor2 = array_ops.concat([tensor2a, tensor2b], 3)
        tensor3 = self.lf.Conv_layer(tensor, [1, 448, 1], True, var_pref + "br3_cv1_")
        tensor3 = self.lf.Conv_layer(tensor3, [3, 384, 1], True, var_pref + "br3_cv2_")
        tensor3a = self.lf.Conv_layer(tensor3, [[1, 3], 384, 1], True, var_pref + "br3_cv3a_")
        tensor3b = self.lf.Conv_layer(tensor3, [[3, 1], 384, 1], True, var_pref + "br3_cv3b_")
        tensor3 = array_ops.concat([tensor3a, tensor3b], 3)
        tensor4 = self.lf.Pool_layer(tensor, False, [3, 1], True)
        tensor4 = self.lf.Conv_layer(tensor4, [1, 192, 1], True, var_pref + "br4_cv1_")
        return array_ops.concat([tensor1, tensor2, tensor3, tensor4], 3, name = name)

    def infer(self, tensor):
        # 299 x 299 x 3
        # front layers
        tensor = self.lf.Conv_layer(tensor, [3, 32, 2], False, "fr_cv1_")
        # 149 x 149 x 32
        tensor = self.lf.Conv_layer(tensor, [3, 32, 1], False, "fr_cv2_")
        # 147 x 147 x 32
        tensor = self.lf.Conv_layer(tensor, [3, 64, 1], True, "fr_cv3_")
        # 147 x 147 x 64
        tensor = self.lf.Pool_layer(tensor, True, [3, 2], False)
        # 73 x 73 x 64
        tensor = self.lf.Conv_layer(tensor, [1, 80, 1], False, "fr_cv4_")
        # 73 x 73 x 80
        tensor = self.lf.Conv_layer(tensor, [3, 192, 1], False, "fr_cv5_")
        # 71 x 71 x 192
        tensor = self.lf.Pool_layer(tensor, True, [3, 2], False, name = "front_out")
        # 35 x 35 x 192

        # inception layers
        tensor = self.incep_block_a(tensor, 32, "ic1_", "incep_block1")
        # 35 x 35 x 256
        tensor = self.incep_block_a(tensor, 64, "ic2_", "incep_block2")
        # 35 x 35 x 288
        tensor = self.incep_block_a(tensor, 64, "ic3_", "incep_block3")
        # 35 x 35 x 288
        tensor = self.incep_block_4(tensor)
        # 17 x 17 x 768
        tensor = self.incep_block_b(tensor, 128, "ic5_", "incep_block5")
        # 17 x 17 x 768
        tensor = self.incep_block_b(tensor, 160, "ic6_", "incep_block6")
        # 17 x 17 x 768
        tensor = self.incep_block_b(tensor, 160, "ic7_", "incep_block7")
        # 17 x 17 x 768
        tensor = self.incep_block_b(tensor, 192, "ic8_", "incep_block8")
        # 17 x 17 x 768
        tensor = self.incep_block_9(tensor)
        # 8 x 8 x 1280
        tensor = self.incep_block_c(tensor, "ic10_", "incep_block10")
        # 8 x 8 x 2048
        tensor = self.incep_block_c(tensor, "ic11_", "incep_block11")
        # 8 x 8 x 2048
        tensor = self.lf.Pool_layer(tensor, False, [8, 1], False, name = "bottleneck")
        # 1 x 1 x 2048
        tensor_bottleneck = tensor

        # back layers
        tensor = tf.reshape(tensor, [-1, tensor.get_shape().as_list()[3]])
        for i in range(len(self.layout_fc_size)):
            tensor = self.lf.Fc_layer(tensor, self.layout_fc_size[i], True, "fc_%d_" % (i + 1))
        tensor = self.lf.Fc_layer(tensor, self.layout_output_size, False, "fc_out_", name = "y")
        return tensor, tensor_bottleneck

    def train(self):
        self.lf = networks.LayerFactory(self.arg_weights_stddev,
            tf.contrib.layers.l2_regularizer(self.arg_regularization_rate))
        
        x = tf.placeholder(tf.float32, [None, INPUT_WIDTH, INPUT_WIDTH, INPUT_DEPTH], name = "x")
        y_ = tf.placeholder(tf.float32, [None, self.layout_output_size], name = "y_")
        i_step = tf.Variable(0, trainable = False)

        y, _ = self.infer(x)
        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits = y, labels = tf.argmax(y_, 1))
        loss = tf.reduce_mean(cross_entropy) + tf.add_n(tf.get_collection(networks.L2_COLLECTION_NAME))
        train_op = tf.train.AdamOptimizer(self.arg_adam_learning_rate_base).minimize(loss, global_step = i_step)
        return x, y, y_, train_op, loss, i_step
