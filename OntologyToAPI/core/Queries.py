GET_METADATA_QUERY = """
        SELECT ?m ?t ?d ?q ?ct ?tc
        WHERE {
          ?m <http://www.cedri.com/OntologyToAPI-Metadata#hasSource> ?s .
          ?m <http://www.cedri.com/OntologyToAPI-Metadata#hasType> ?t .
          ?s <http://www.cedri.com/OntologyToAPI-Metadata#hasQuery> ?q .
          ?s <http://www.cedri.com/OntologyToAPI-Metadata#hasDescription> ?d .
          ?s <http://www.cedri.com/OntologyToAPI-Metadata#hasCommunicationTechnology> ?ct .
          ?ct <http://www.cedri.com/OntologyToAPI-Communications#usesTechnology> ?tc .
        }
        """

GET_COMMUNICATION_TECH_ARGS_QUERY = """
        SELECT ?arg ?argv
        WHERE {
          ?s <http://www.cedri.com/OntologyToAPI-Metadata#hasCommunicationTechnology> ?ct .
          ?ct ?arg ?argv .
          FILTER(?arg != <http://www.cedri.com/OntologyToAPI-Communications#usesTechnology> &&
          ?arg != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> &&
          ?ct = <"""

GET_BM_NAME_QUERY = """
        SELECT ?bm
        WHERE {
          ?bm rdfs:subClassOf <http://www.cedri.com/OntologyToAPI-BusinessModel#BusinessModel> .
        }
        """

GET_REQUIRED_MD_FOR_BM_QUERY = """
        SELECT ?bm ?rm
        WHERE {
          ?bm <http://www.cedri.com/OntologyToAPI-BusinessModel#requiresMetadata> ?rm .
          FILTER (?bm = <"""

GET_REQUIRED_PARAMETERS_FOR_BM_QUERY = """
        SELECT ?bm ?pl ?pt
        WHERE {
          ?bm <http://www.cedri.com/OntologyToAPI-BusinessModel#hasParameter> ?p .
          ?p <http://www.cedri.com/OntologyToAPI-BusinessModel#hasParameterLabel> ?pl .
          ?p <http://www.cedri.com/OntologyToAPI-BusinessModel#hasParameterType> ?pt .
          FILTER (?bm = <"""

GET_EXTERNAL_CODE_FOR_BM_QUERY = """
        SELECT ?bm ?ec ?pf ?rl ?hf
        WHERE {
          ?bm <http://www.cedri.com/OntologyToAPI-BusinessModel#hasExternalCode> ?ec .
          ?ec <http://www.cedri.com/OntologyToAPI-ExternalCode#hasPythonFile> ?pf .
          ?ec <http://www.cedri.com/OntologyToAPI-ExternalCode#requiresLib> ?rl .
          ?ec <http://www.cedri.com/OntologyToAPI-ExternalCode#hasFunction> ?hf .
        }
        """