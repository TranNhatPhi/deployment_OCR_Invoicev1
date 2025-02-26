import paddle
import math
from x2paddle.op_mapper.pytorch2paddle import pytorch_custom_layer as x2paddle_nn

class DetectionModel(paddle.nn.Layer):
    def __init__(self):
        super(DetectionModel, self).__init__()
        self.conv2d0 = paddle.nn.Conv2D(stride=2, padding=1, out_channels=16, kernel_size=(3, 3), in_channels=3)
        self.silu0 = paddle.nn.Silu()
        self.conv2d1 = paddle.nn.Conv2D(stride=2, padding=1, out_channels=32, kernel_size=(3, 3), in_channels=16)
        self.silu1 = paddle.nn.Silu()
        self.conv2d2 = paddle.nn.Conv2D(out_channels=32, kernel_size=(1, 1), in_channels=32)
        self.silu2 = paddle.nn.Silu()
        self.conv2d3 = paddle.nn.Conv2D(padding=1, out_channels=16, kernel_size=(3, 3), in_channels=16)
        self.silu3 = paddle.nn.Silu()
        self.conv2d4 = paddle.nn.Conv2D(padding=1, out_channels=16, kernel_size=(3, 3), in_channels=16)
        self.silu4 = paddle.nn.Silu()
        self.conv2d5 = paddle.nn.Conv2D(out_channels=32, kernel_size=(1, 1), in_channels=48)
        self.silu5 = paddle.nn.Silu()
        self.conv2d6 = paddle.nn.Conv2D(stride=2, padding=1, out_channels=64, kernel_size=(3, 3), in_channels=32)
        self.silu6 = paddle.nn.Silu()
        self.conv2d7 = paddle.nn.Conv2D(out_channels=64, kernel_size=(1, 1), in_channels=64)
        self.silu7 = paddle.nn.Silu()
        self.conv2d8 = paddle.nn.Conv2D(padding=1, out_channels=32, kernel_size=(3, 3), in_channels=32)
        self.silu8 = paddle.nn.Silu()
        self.conv2d9 = paddle.nn.Conv2D(padding=1, out_channels=32, kernel_size=(3, 3), in_channels=32)
        self.silu9 = paddle.nn.Silu()
        self.conv2d10 = paddle.nn.Conv2D(padding=1, out_channels=32, kernel_size=(3, 3), in_channels=32)
        self.silu10 = paddle.nn.Silu()
        self.conv2d11 = paddle.nn.Conv2D(padding=1, out_channels=32, kernel_size=(3, 3), in_channels=32)
        self.silu11 = paddle.nn.Silu()
        self.conv2d12 = paddle.nn.Conv2D(out_channels=64, kernel_size=(1, 1), in_channels=128)
        self.silu12 = paddle.nn.Silu()
        self.conv2d13 = paddle.nn.Conv2D(stride=2, padding=1, out_channels=128, kernel_size=(3, 3), in_channels=64)
        self.silu13 = paddle.nn.Silu()
        self.conv2d14 = paddle.nn.Conv2D(out_channels=128, kernel_size=(1, 1), in_channels=128)
        self.silu14 = paddle.nn.Silu()
        self.conv2d15 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu15 = paddle.nn.Silu()
        self.conv2d16 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu16 = paddle.nn.Silu()
        self.conv2d17 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu17 = paddle.nn.Silu()
        self.conv2d18 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu18 = paddle.nn.Silu()
        self.conv2d19 = paddle.nn.Conv2D(out_channels=128, kernel_size=(1, 1), in_channels=256)
        self.silu19 = paddle.nn.Silu()
        self.conv2d20 = paddle.nn.Conv2D(stride=2, padding=1, out_channels=256, kernel_size=(3, 3), in_channels=128)
        self.silu20 = paddle.nn.Silu()
        self.conv2d21 = paddle.nn.Conv2D(out_channels=256, kernel_size=(1, 1), in_channels=256)
        self.silu21 = paddle.nn.Silu()
        self.conv2d22 = paddle.nn.Conv2D(padding=1, out_channels=128, kernel_size=(3, 3), in_channels=128)
        self.silu22 = paddle.nn.Silu()
        self.conv2d23 = paddle.nn.Conv2D(padding=1, out_channels=128, kernel_size=(3, 3), in_channels=128)
        self.silu23 = paddle.nn.Silu()
        self.conv2d24 = paddle.nn.Conv2D(out_channels=256, kernel_size=(1, 1), in_channels=384)
        self.silu24 = paddle.nn.Silu()
        self.conv2d25 = paddle.nn.Conv2D(out_channels=128, kernel_size=(1, 1), in_channels=256)
        self.silu25 = paddle.nn.Silu()
        self.pool2d0 = paddle.nn.MaxPool2D(kernel_size=[5, 5], stride=1, padding=2)
        self.pool2d1 = paddle.nn.MaxPool2D(kernel_size=[5, 5], stride=1, padding=2)
        self.pool2d2 = paddle.nn.MaxPool2D(kernel_size=[5, 5], stride=1, padding=2)
        self.conv2d26 = paddle.nn.Conv2D(out_channels=256, kernel_size=(1, 1), in_channels=512)
        self.silu26 = paddle.nn.Silu()
        self.conv2d27 = paddle.nn.Conv2D(out_channels=128, kernel_size=(1, 1), in_channels=384)
        self.silu27 = paddle.nn.Silu()
        self.conv2d28 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu28 = paddle.nn.Silu()
        self.conv2d29 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu29 = paddle.nn.Silu()
        self.conv2d30 = paddle.nn.Conv2D(out_channels=128, kernel_size=(1, 1), in_channels=192)
        self.silu30 = paddle.nn.Silu()
        self.conv2d31 = paddle.nn.Conv2D(out_channels=64, kernel_size=(1, 1), in_channels=192)
        self.silu31 = paddle.nn.Silu()
        self.conv2d32 = paddle.nn.Conv2D(padding=1, out_channels=32, kernel_size=(3, 3), in_channels=32)
        self.silu32 = paddle.nn.Silu()
        self.conv2d33 = paddle.nn.Conv2D(padding=1, out_channels=32, kernel_size=(3, 3), in_channels=32)
        self.silu33 = paddle.nn.Silu()
        self.conv2d34 = paddle.nn.Conv2D(out_channels=64, kernel_size=(1, 1), in_channels=96)
        self.silu34 = paddle.nn.Silu()
        self.conv2d35 = paddle.nn.Conv2D(stride=2, padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu35 = paddle.nn.Silu()
        self.conv2d36 = paddle.nn.Conv2D(out_channels=128, kernel_size=(1, 1), in_channels=192)
        self.silu36 = paddle.nn.Silu()
        self.conv2d37 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu37 = paddle.nn.Silu()
        self.conv2d38 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu38 = paddle.nn.Silu()
        self.conv2d39 = paddle.nn.Conv2D(out_channels=128, kernel_size=(1, 1), in_channels=192)
        self.silu39 = paddle.nn.Silu()
        self.conv2d40 = paddle.nn.Conv2D(stride=2, padding=1, out_channels=128, kernel_size=(3, 3), in_channels=128)
        self.silu40 = paddle.nn.Silu()
        self.conv2d41 = paddle.nn.Conv2D(out_channels=256, kernel_size=(1, 1), in_channels=384)
        self.silu41 = paddle.nn.Silu()
        self.conv2d42 = paddle.nn.Conv2D(padding=1, out_channels=128, kernel_size=(3, 3), in_channels=128)
        self.silu42 = paddle.nn.Silu()
        self.conv2d43 = paddle.nn.Conv2D(padding=1, out_channels=128, kernel_size=(3, 3), in_channels=128)
        self.silu43 = paddle.nn.Silu()
        self.conv2d44 = paddle.nn.Conv2D(out_channels=256, kernel_size=(1, 1), in_channels=384)
        self.silu44 = paddle.nn.Silu()
        self.x635 = self.create_parameter(dtype='float32', shape=(1, 8400), default_initializer=paddle.nn.initializer.Constant(value=0.0))
        self.conv2d45 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu45 = paddle.nn.Silu()
        self.conv2d46 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu46 = paddle.nn.Silu()
        self.conv2d47 = paddle.nn.Conv2D(out_channels=64, kernel_size=(1, 1), in_channels=64)
        self.conv2d48 = paddle.nn.Conv2D(padding=1, out_channels=80, kernel_size=(3, 3), in_channels=64)
        self.silu47 = paddle.nn.Silu()
        self.conv2d49 = paddle.nn.Conv2D(padding=1, out_channels=80, kernel_size=(3, 3), in_channels=80)
        self.silu48 = paddle.nn.Silu()
        self.conv2d50 = paddle.nn.Conv2D(out_channels=80, kernel_size=(1, 1), in_channels=80)
        self.conv2d51 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=128)
        self.silu49 = paddle.nn.Silu()
        self.conv2d52 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu50 = paddle.nn.Silu()
        self.conv2d53 = paddle.nn.Conv2D(out_channels=64, kernel_size=(1, 1), in_channels=64)
        self.conv2d54 = paddle.nn.Conv2D(padding=1, out_channels=80, kernel_size=(3, 3), in_channels=128)
        self.silu51 = paddle.nn.Silu()
        self.conv2d55 = paddle.nn.Conv2D(padding=1, out_channels=80, kernel_size=(3, 3), in_channels=80)
        self.silu52 = paddle.nn.Silu()
        self.conv2d56 = paddle.nn.Conv2D(out_channels=80, kernel_size=(1, 1), in_channels=80)
        self.conv2d57 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=256)
        self.silu53 = paddle.nn.Silu()
        self.conv2d58 = paddle.nn.Conv2D(padding=1, out_channels=64, kernel_size=(3, 3), in_channels=64)
        self.silu54 = paddle.nn.Silu()
        self.conv2d59 = paddle.nn.Conv2D(out_channels=64, kernel_size=(1, 1), in_channels=64)
        self.conv2d60 = paddle.nn.Conv2D(padding=1, out_channels=80, kernel_size=(3, 3), in_channels=256)
        self.silu55 = paddle.nn.Silu()
        self.conv2d61 = paddle.nn.Conv2D(padding=1, out_channels=80, kernel_size=(3, 3), in_channels=80)
        self.silu56 = paddle.nn.Silu()
        self.conv2d62 = paddle.nn.Conv2D(out_channels=80, kernel_size=(1, 1), in_channels=80)
        self.softmax0 = paddle.nn.Softmax(axis=1)
        self.conv2d63 = paddle.nn.Conv2D(out_channels=1, kernel_size=(1, 1), bias_attr=False, in_channels=16)
        self.x854 = self.create_parameter(dtype='float32', shape=(1, 2, 8400), default_initializer=paddle.nn.initializer.Constant(value=0.0))
        self.sigmoid0 = paddle.nn.Sigmoid()

    def forward(self, x0):
        x45 = self.conv2d0(x0)
        x46 = self.silu0(x45)
        x57 = self.conv2d1(x46)
        x58 = self.silu1(x57)
        x73 = self.conv2d2(x58)
        x74 = self.silu2(x73)
        x76 = paddle.split(x=x74, num_or_sections=2, axis=1)
        x77, x78 = x76
        x88 = self.conv2d3(x78)
        x89 = self.silu3(x88)
        x97 = self.conv2d4(x89)
        x98 = self.silu4(x97)
        x99 = x78 + x98
        x100 = [x77, x78, x99]
        x101 = paddle.concat(x=x100, axis=1)
        x109 = self.conv2d5(x101)
        x110 = self.silu5(x109)
        x121 = self.conv2d6(x110)
        x122 = self.silu6(x121)
        x139 = self.conv2d7(x122)
        x140 = self.silu7(x139)
        x142 = paddle.split(x=x140, num_or_sections=2, axis=1)
        x143, x144 = x142
        x154 = self.conv2d8(x144)
        x155 = self.silu8(x154)
        x163 = self.conv2d9(x155)
        x164 = self.silu9(x163)
        x165 = x144 + x164
        x175 = self.conv2d10(x165)
        x176 = self.silu10(x175)
        x184 = self.conv2d11(x176)
        x185 = self.silu11(x184)
        x186 = x165 + x185
        x187 = [x143, x144, x165, x186]
        x188 = paddle.concat(x=x187, axis=1)
        x196 = self.conv2d12(x188)
        x197 = self.silu12(x196)
        x208 = self.conv2d13(x197)
        x209 = self.silu13(x208)
        x226 = self.conv2d14(x209)
        x227 = self.silu14(x226)
        x229 = paddle.split(x=x227, num_or_sections=2, axis=1)
        x230, x231 = x229
        x241 = self.conv2d15(x231)
        x242 = self.silu15(x241)
        x250 = self.conv2d16(x242)
        x251 = self.silu16(x250)
        x252 = x231 + x251
        x262 = self.conv2d17(x252)
        x263 = self.silu17(x262)
        x271 = self.conv2d18(x263)
        x272 = self.silu18(x271)
        x273 = x252 + x272
        x274 = [x230, x231, x252, x273]
        x275 = paddle.concat(x=x274, axis=1)
        x283 = self.conv2d19(x275)
        x284 = self.silu19(x283)
        x295 = self.conv2d20(x284)
        x296 = self.silu20(x295)
        x311 = self.conv2d21(x296)
        x312 = self.silu21(x311)
        x314 = paddle.split(x=x312, num_or_sections=2, axis=1)
        x315, x316 = x314
        x326 = self.conv2d22(x316)
        x327 = self.silu22(x326)
        x335 = self.conv2d23(x327)
        x336 = self.silu23(x335)
        x337 = x316 + x336
        x338 = [x315, x316, x337]
        x339 = paddle.concat(x=x338, axis=1)
        x347 = self.conv2d24(x339)
        x348 = self.silu24(x347)
        x361 = self.conv2d25(x348)
        x362 = self.silu25(x361)
        x367 = self.pool2d0(x362)
        x372 = self.pool2d1(x367)
        x377 = self.pool2d2(x372)
        x378 = [x362, x367, x372, x377]
        x379 = paddle.concat(x=x378, axis=1)
        x387 = self.conv2d26(x379)
        x388 = self.silu26(x387)
        x390 = [2.0, 2.0]
        x391 = paddle.nn.functional.interpolate(x=x388, scale_factor=x390, mode='nearest')
        x393 = [x391, x284]
        x394 = paddle.concat(x=x393, axis=1)
        x409 = self.conv2d27(x394)
        x410 = self.silu27(x409)
        x412 = paddle.split(x=x410, num_or_sections=2, axis=1)
        x413, x414 = x412
        x424 = self.conv2d28(x414)
        x425 = self.silu28(x424)
        x433 = self.conv2d29(x425)
        x434 = self.silu29(x433)
        x435 = [x413, x414, x434]
        x436 = paddle.concat(x=x435, axis=1)
        x444 = self.conv2d30(x436)
        x445 = self.silu30(x444)
        x447 = [2.0, 2.0]
        x448 = paddle.nn.functional.interpolate(x=x445, scale_factor=x447, mode='nearest')
        x450 = [x448, x197]
        x451 = paddle.concat(x=x450, axis=1)
        x466 = self.conv2d31(x451)
        x467 = self.silu31(x466)
        x469 = paddle.split(x=x467, num_or_sections=2, axis=1)
        x470, x471 = x469
        x481 = self.conv2d32(x471)
        x482 = self.silu32(x481)
        x490 = self.conv2d33(x482)
        x491 = self.silu33(x490)
        x492 = [x470, x471, x491]
        x493 = paddle.concat(x=x492, axis=1)
        x501 = self.conv2d34(x493)
        x502 = self.silu34(x501)
        x513 = self.conv2d35(x502)
        x514 = self.silu35(x513)
        x516 = [x514, x445]
        x517 = paddle.concat(x=x516, axis=1)
        x532 = self.conv2d36(x517)
        x533 = self.silu36(x532)
        x535 = paddle.split(x=x533, num_or_sections=2, axis=1)
        x536, x537 = x535
        x547 = self.conv2d37(x537)
        x548 = self.silu37(x547)
        x556 = self.conv2d38(x548)
        x557 = self.silu38(x556)
        x558 = [x536, x537, x557]
        x559 = paddle.concat(x=x558, axis=1)
        x567 = self.conv2d39(x559)
        x568 = self.silu39(x567)
        x579 = self.conv2d40(x568)
        x580 = self.silu40(x579)
        x582 = [x580, x388]
        x583 = paddle.concat(x=x582, axis=1)
        x598 = self.conv2d41(x583)
        x599 = self.silu41(x598)
        x601 = paddle.split(x=x599, num_or_sections=2, axis=1)
        x602, x603 = x601
        x613 = self.conv2d42(x603)
        x614 = self.silu42(x613)
        x622 = self.conv2d43(x614)
        x623 = self.silu43(x622)
        x624 = [x602, x603, x623]
        x625 = paddle.concat(x=x624, axis=1)
        x633 = self.conv2d44(x625)
        x634 = self.silu44(x633)
        x635 = self.x635
        x636 = 2
        x638 = 2
        x639 = 1
        x665 = self.conv2d45(x502)
        x666 = self.silu45(x665)
        x674 = self.conv2d46(x666)
        x675 = self.silu46(x674)
        x682 = self.conv2d47(x675)
        x693 = self.conv2d48(x502)
        x694 = self.silu47(x693)
        x702 = self.conv2d49(x694)
        x703 = self.silu48(x702)
        x710 = self.conv2d50(x703)
        x711 = [x682, x710]
        x712 = paddle.concat(x=x711, axis=1)
        x723 = self.conv2d51(x568)
        x724 = self.silu49(x723)
        x732 = self.conv2d52(x724)
        x733 = self.silu50(x732)
        x740 = self.conv2d53(x733)
        x751 = self.conv2d54(x568)
        x752 = self.silu51(x751)
        x760 = self.conv2d55(x752)
        x761 = self.silu52(x760)
        x768 = self.conv2d56(x761)
        x769 = [x740, x768]
        x770 = paddle.concat(x=x769, axis=1)
        x781 = self.conv2d57(x634)
        x782 = self.silu53(x781)
        x790 = self.conv2d58(x782)
        x791 = self.silu54(x790)
        x798 = self.conv2d59(x791)
        x809 = self.conv2d60(x634)
        x810 = self.silu55(x809)
        x818 = self.conv2d61(x810)
        x819 = self.silu56(x818)
        x826 = self.conv2d62(x819)
        x827 = [x798, x826]
        x828 = paddle.concat(x=x827, axis=1)
        x830 = paddle.reshape(x=x712, shape=[1, 144, -1])
        x832 = paddle.reshape(x=x770, shape=[1, 144, -1])
        x834 = paddle.reshape(x=x828, shape=[1, 144, -1])
        x835 = [x830, x832, x834]
        x836 = paddle.concat(x=x835, axis=2)
        x838 = paddle.split(x=x836, num_or_sections=[64, 80], axis=1)
        x839, x840 = x838
        x843 = paddle.reshape(x=x839, shape=[1, 4, 16, 8400])
        x844_shape = x843.shape
        x844_len = len(x844_shape)
        x844_list = []
        for i in range(x844_len):
            x844_list.append(i)
        if x638 < 0:
            x638_new = x638 + x844_len
        else:
            x638_new = x638
        if x639 < 0:
            x639_new = x639 + x844_len
        else:
            x639_new = x639
        x844_list[x638_new] = x639_new
        x844_list[x639_new] = x638_new
        x844 = paddle.transpose(x=x843, perm=x844_list)
        x845 = self.softmax0(x844)
        x851 = self.conv2d63(x845)
        x853 = paddle.reshape(x=x851, shape=[1, 4, 8400])
        x854 = self.x854
        x855 = paddle.split(x=x853, num_or_sections=2, axis=1)
        x856, x857 = x855
        x858 = x854 - x856
        x859 = x854 + x857
        x860 = x858 + x859
        x861 = x860 / x636
        x862 = x859 - x858
        x863 = [x861, x862]
        x864 = paddle.concat(x=x863, axis=1)
        x865 = x864 * x635
        x866 = self.sigmoid0(x840)
        x867 = [x865, x866]
        x868 = paddle.concat(x=x867, axis=1)
        return x868

def main(x0):
    # There are 1 inputs.
    # x0: shape-[1, 3, 640, 640], type-float32.
    paddle.disable_static()
    params = paddle.load(r'D:\savecode\pythonProjectOCR8\yolov8n_paddle_model\model.pdparams')
    model = DetectionModel()
    model.set_dict(params, use_structured_name=True)
    model.eval()
    out = model(x0)
    return out
