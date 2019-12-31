bamboo_dependencies_dict = {
    "exceptions": ["DownloadFailedException", "InvalidCredentialsException", "AbsolutePathException"],
    "helpers": 
        [
            "decrypt", "grab_parent_dir", "convert_to_absolute", "grab_connector", "random_char", 
            "dict_product", "expand_path", "query_to_df", "process_uri_wildcards", "wildcard_matches", 
            "table_has_duplicates"
        ],
    "logger": ["logger"],
    "models": 
        [
            "BasePipeline", "LoopHelper", "EasyPipeline", "Parameter", "LinearPipelineExecutor", 
            "GraphPipelineExecutor", "PipelineStep", "ParallelizedStep", "Node", "EndNode", 
            "ComplexPipelineExecutor", "AdvancedPipelineExecutor", "ResultWrapper"
        ],
    "params_helper": ["find_param", "extract"],
    "steps": 
        [
            "DownloadStep", "WildcardDownloadStep", "LoadStep", "LoadStepDynamic", "UnzipStep", 
            "UnzipToFolderStep", "CleanupFileStep", "WriteDFToDiskStep", "SCPTransferStep", 
            "SSHCommandStep", "LockStep", "SSHTunnelStartStep", "SSHTunnelCloseStep", "IngestMonetStep"
        ]
}


def camelcase_to_snakecase(str):
    words = [[str[0]]] 
  
    for c in str[1:]: 
        if words[-1][-1].islower() and c.isupper(): 
            words.append(list(c)) 
        else: 
            words[-1].append(c) 
  
    words = [''.join(word).lower() for word in words]

    return '_'.join(words)
