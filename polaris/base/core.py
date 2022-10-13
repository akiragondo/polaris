from abc import abstractmethod
from enum import Enum, auto
from utils import has_method
import types
from typing import List

class ProcessType(Enum):
    PREPROCESS = auto()
    MODEL = auto()

class ProcessImportance(Enum):
    OBLIGATORY = auto()
    OPTIONAL = auto()


class Process:
    def __init__(self, process,function_type : ProcessType, process_importance : ProcessImportance,**kwargs):
        self.process = process
        self.function_type = function_type
        self.kwargs = kwargs
        self.process_importance = process_importance

    @abstractmethod
    def run(self, input_data):
        """
        input_data: Input for processing with Process object
        :return: Transformed data through the processing funciton
        """
        pass

    def save(self):
        """
        :return: Something that can be used to reference this particular function with these parameters
        """
        pass


class StandardProcess(Process):
    def __init__(self, process,function_type : ProcessType, **kwargs):
        super().__init__(process, function_type, **kwargs)

    def run(self, input_data):
        if isinstance(self.process, types.FunctionType):
            return self.process(input_data)
        else:
            if has_method(self.process, "fit_predict"):
                return self.process.fit_predict(input_data)
            elif has_method(self.process, "fit_transform"):
                return self.process.fit_transform(input_data)
            elif has_method(self.process, "fit"):
                if has_method(self.process, "transform"):
                    self.process = self.process.fit(input_data)
                    return self.process.transform(input_data)
                elif has_method(self.process, "predict"):
                    self.process = self.process.fit(input_data)
                    return self.process.predict(input_data)
        raise TypeError


class Pipeline:
    process_list = List[Process]
    def __init__(self, process_sequence : process_list):
        self.process_sequence = {
            f"{process}_{index}" : process
            for index, process in enumerate(process_sequence)
        }

    def get_process_list(self):
        return self.process_sequence

    def run_pipeline(self):

