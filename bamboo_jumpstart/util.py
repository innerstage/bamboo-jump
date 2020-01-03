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


def camelcase_to_snakecase(name):
    start = []
    words = []
  
    for index, char in enumerate(name): 
        if char.isupper():
            start.append(index)

    for i in range(len(start)-1):
        words.append(name[start[i]:start[i+1]])
    words.append(name[start[-1]:])

    lower_words = [w.lower() for w in words]

    return "_".join(lower_words)


if __name__ == "__main__":
    print(camelcase_to_snakecase("WillIAm"))