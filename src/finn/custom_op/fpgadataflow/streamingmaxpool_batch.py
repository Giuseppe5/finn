from finn.custom_op.fpgadataflow import HLSCustomOp


class StreamingMaxPool_Batch(HLSCustomOp):
    def get_nodeattr_types(self):
        my_attrs = {
            "ImgDim": ("i", True, 0),
            "PoolDim": ("i", True, 0),
            "NumChannels": ("i", True, 0),
        }
        my_attrs.update(super().get_nodeattr_types())
        return my_attrs

    def make_shape_compatible_op(self):
        pass

    def infer_node_datatype(self, model):
        pass

    def global_includes(self):
        self.code_gen_dict["$GLOBALS$"] = ['#include "maxpool.h"']

    def defines(self):
        numReps = 2
        self.code_gen_dict["$DEFINES$"] = [
            """#define ImgDim {}\n #define PoolDim {}\n
            #define NumChannels {}\n #define numReps {}""".format(
                self.get_nodeattr("ImgDim"),
                self.get_nodeattr("PoolDim"),
                self.get_nodeattr("NumChannels"),
                numReps,
            )
        ]

    def read_npy_data(self):
        node = self.onnx_node
        code_gen_dir = self.get_nodeattr("code_gen_dir")
        # c++ code to read out an npy file
        # and put it in hls::stream in the correct order
        self.code_gen_dict["$READNPYDATA$"] = []
        input_ind = 0
        input_file_names = []
        for inputs in node.input:
            input_file_names.append("{}/input_{}.npy".format(code_gen_dir, input_ind))
            input_ind += 1

        input_ind = 0
        for input_file in input_file_names:
            self.code_gen_dict["$READNPYDATA$"].append(
                """cnpy::NpyArray arr = cnpy::npy_load("{}");\n
                float* loaded_data{} = arr.data<float>();""".format(
                    input_file, input_ind
                )
            )
            self.code_gen_dict["$READNPYDATA$"].append(
                """int num_values = 1; \n
                for(int i = 0; i < arr.shape.size(); i++){\n
                num_values *= arr.shape[i]; \n }"""
            )
            self.code_gen_dict["$READNPYDATA$"].append(
                "ap_uint<{}> dat;".format(self.get_nodeattr("NumChannels"))
            )
            self.code_gen_dict["$READNPYDATA$"].append(
                "for(int i=0; i < num_values/{}; i++){{".format(
                    self.get_nodeattr("NumChannels")
                )
            )
            for channel in range(self.get_nodeattr("NumChannels")):
                self.code_gen_dict["$READNPYDATA$"].append(
                    "dat.range({},{}) = loaded_data{}[i+((num_values/{})*{})];".format(
                        channel,
                        channel,
                        input_ind,
                        self.get_nodeattr("NumChannels"),
                        channel,
                    )
                )
            self.code_gen_dict["$READNPYDATA$"].append("in{} << dat;".format(input_ind))
            self.code_gen_dict["$READNPYDATA$"].append("}")
            input_ind += 1

    def strm_decl(self):
        node = self.onnx_node
        self.code_gen_dict["$STREAMDECLARATIONS$"] = []
        input_ind = 0
        for inputs in node.input:
            self.code_gen_dict["$STREAMDECLARATIONS$"].append(
                'hls::stream<ap_uint<{}>> in{} ("in{}");'.format(
                    self.get_nodeattr("NumChannels"), input_ind, input_ind
                )
            )
            input_ind += 1
        self.code_gen_dict["$STREAMDECLARATIONS$"].append(
            'hls::stream<ap_uint<{}>> out ("out");'.format(
                self.get_nodeattr("NumChannels")
            )
        )

    def docompute(self):
        node = self.onnx_node
        self.code_gen_dict["$DOCOMPUTE$"] = [
            "{}<ImgDim, PoolDim, NumChannels>(in0, out, numReps);".format(node.op_type)
        ]

    def dataoutstrm(self):
        self.code_gen_dict["$DATAOUTSTREAM$"] = [
            "ap_uint<{}> out_data;\n std::vector<ap_uint<{}>> out_data_vector;".format(
                self.get_nodeattr("NumChannels"), self.get_nodeattr("NumChannels")
            )
        ]
        self.code_gen_dict["$DATAOUTSTREAM$"].append("while(out.read_nb(out_data)){")
        self.code_gen_dict["$DATAOUTSTREAM$"].append(
            "out_data_vector.push_back(out_data);\n}"
        )
        self.code_gen_dict["$DATAOUTSTREAM$"].append(
            "std::vector<float> output_data_vector;"
        )
        self.code_gen_dict["$DATAOUTSTREAM$"].append(
            """for(std::vector<ap_uint<{}>>::iterator it = out_data_vector.begin();
            it != out_data_vector.end(); ++it){{""".format(
                self.get_nodeattr("NumChannels")
            )
        )
        self.code_gen_dict["$DATAOUTSTREAM$"].append(
            "ap_uint<{}> output_data = *it;".format(self.get_nodeattr("NumChannels"))
        )
        for channel in range(self.get_nodeattr("NumChannels")):
            self.code_gen_dict["$DATAOUTSTREAM$"].append(
                "output_data_vector.push_back(output_data.range({},{}));".format(
                    channel, channel
                )
            )
        self.code_gen_dict["$DATAOUTSTREAM$"].append("}")

    def save_as_npy(self):
        code_gen_dir = self.get_nodeattr("code_gen_dir")
        numReps = 1
        self.code_gen_dict["$SAVEASCNPY$"] = [
            """cnpy::npy_save("{}/output.npy",&output_data_vector[0],
            {{{},{},{}}},"w");""".format(
                code_gen_dir,
                numReps,
                self.get_nodeattr("NumChannels"),
                int(self.get_nodeattr("ImgDim") / self.get_nodeattr("PoolDim")),
                int(self.get_nodeattr("ImgDim") / self.get_nodeattr("PoolDim")),
            )
        ]