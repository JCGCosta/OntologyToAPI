GET_METADATA_QUERY = """
        SELECT ?m ?t ?d ?q ?ct ?tc
        WHERE {
          ?m <http://www.cedri.com/SmartLEM-Metadata#hasSource> ?s .
          ?m <http://www.cedri.com/SmartLEM-Metadata#hasType> ?t .
          ?s <http://www.cedri.com/SmartLEM-Metadata#hasQuery> ?q .
          ?s <http://www.cedri.com/SmartLEM-Metadata#hasDescription> ?d .
          ?s <http://www.cedri.com/SmartLEM-Metadata#hasCommunicationTechnology> ?ct .
          ?ct <http://www.cedri.com/SmartLEM-Communications#usesTechnology> ?tc .
        }
        """

GET_COMMUNICATION_TECH_ARGS_QUERY = """
        SELECT ?arg ?argv
        WHERE {
          ?s <http://www.cedri.com/SmartLEM-Metadata#hasCommunicationTechnology> ?ct .
          ?ct ?arg ?argv .
          FILTER(?arg != <http://www.cedri.com/SmartLEM-Communications#usesTechnology> &&
          ?arg != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> &&
          ?ct = <"""

GET_BM_NAME_QUERY = """
        SELECT ?bm
        WHERE {
          ?bm rdfs:subClassOf <http://www.cedri.com/SmartLEM-BusinessModel#BusinessModel> .
        }
        """

GET_REQUIRED_MD_FOR_BM_QUERY = """
        SELECT ?bm ?rm
        WHERE {
          ?bm <http://www.cedri.com/SmartLEM-BusinessModel#requiresMetadata> ?rm .
          FILTER (?bm = <"""

GET_REQUIRED_PARAMETERS_FOR_BM_QUERY = """
        SELECT ?bm ?pl ?pt
        WHERE {
          ?bm <http://www.cedri.com/SmartLEM-BusinessModel#hasParameter> ?p .
          ?p <http://www.cedri.com/SmartLEM-BusinessModel#hasParameterLabel> ?pl .
          ?p <http://www.cedri.com/SmartLEM-BusinessModel#hasParameterType> ?pt .
          FILTER (?bm = <"""

GET_EXTERNAL_CODE_FOR_BM_QUERY = """
        SELECT ?bm ?ec ?pf ?rl ?hf
        WHERE {
          ?bm <http://www.cedri.com/SmartLEM-BusinessModel#hasExternalCode> ?ec .
          ?ec <http://www.cedri.com/SmartLEM-ExternalCode#hasPythonFile> ?pf .
          ?ec <http://www.cedri.com/SmartLEM-ExternalCode#requiresLib> ?rl .
          ?ec <http://www.cedri.com/SmartLEM-ExternalCode#hasFunction> ?hf .
        }
        """