import pandas as pd
import numpy
from json import loads as load_json
from copy import copy
from math import sqrt, pi
import tensorflow
import os
from bamboo_lib.helpers import grab_connector, query_to_df, grab_connector
from bamboo_lib.logger import logger, logger
from bamboo_lib.models import EasyPipeline, PipelineStep, Parameter

class InitializeStep(PipelineStep):
	def run_step(self, prev, params):
		logger.info("InitializeStep...")
		result = prev

		return result


class IterationStep(PipelineStep):
	def run_step(self, prev, params):
		logger.info("IterationStep...")
		result = prev

		return result


class TransformStep(PipelineStep):
	def run_step(self, prev, params):
		logger.info("TransformStep...")
		result = prev

		return result


class NewPipeline(EasyPipeline):
	@staticmethod
	def parameter_list():
		return [
			Parameter("output-db", dtype=str),
			Parameter("ingest", dtype=bool),
			Parameter("year", dtype=str),
			Parameter("frequency", dtype=str, default_value="A")
		]

	@staticmethod
	def steps(params):
		parent_dir = os.path.join(grab_parent_dir(__file__))

		init_step = InitializeStep()
		wdl_step = WildcardDownloadStep(connector="chile-trade", connector_path=parent_dir)
		iter_step = IterationStep()
		transform_step = TransformStep()
		load_step = LoadStep(
			table_name="",
			connector=params.get("output-db"),
			connector_path=parent_dir,
			if_exists="",
			pk=[]
			dtype= ,
			nullable_list=[]
		)

		sub_steps = [transform_step, load_step] if params.get("ingest") else [transform_step]

		return [init_step, wdl_step, LoopHelper(iter_step=iter_step, sub_steps=sub_steps)]

if __name__ == "__main__":
	new_pipeline = NewPipeline()
	new_pipeline.run(
		{
			"output-db": "",
			"ingest": False,
			"year": "",
			"frequency": "A"
		}
