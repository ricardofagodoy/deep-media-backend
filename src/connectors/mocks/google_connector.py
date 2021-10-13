from connectors.base_connector import BaseConnector
from models.connector import Connector

GOOGLE_MOCK_CONNECTOR_OPTIONS = {
            "ads_accounts": {
                "1835752650:1835752650": [
                    "DMCO_062021_CPA_Trafego"
                ],
                "4890957298:3013036305": [

                ],
                "4890957298:4413234797": [
                    "Website traffic-Search-1"
                ],
                "5451024778:2245083982": [

                ],
                "5451024778:4927215443": [

                ],
                "8752511022:8752511022": [
                    "Garrafa",
                    "BallGame",
                    "Bolos",
                    "Cpg Deep Media Tester"
                ],
                "9124817909:9124817909": [
                    "Teste 1",
                    "Vendas- DSA",
                    "DSA",
                    "[Campanha Display] Responsivo + Remarketing",
                    "[Campanha Search] Branding_Marca",
                    "Campanha PLA Mais vendidos",
                    "[Campanha Search] CONCORRENTES",
                    "[Campanha Display] Responsivo + Remarketing_V2",
                    "[Campanha Search] RLSA #2",
                    "[Campanha Search] Sonho_Baby_Categorias",
                    "Campanha PLA_DM_01",
                    "B4P [Campanha Shopping Teste]",
                    "[ B4p Teste 01 ] Smartshopping",
                    "[Campanha Search] Ortobom",
                    "B4P [Campanha Shopping Teste] Apostas",
                    "B4P [Campanha Shopping]_[DMCO]_[Camas]"
                ]
            },
            "ga_accounts": {
                "111207543": {
                    "name": "ricardofagodoy.github.io",
                    "properties": {
                        "UA-111207543-1": {
                            "custom_metrics": [

                            ],
                            "profiles": [
                                {
                                    "id": "166329541",
                                    "name": "All Web Site Data"
                                }
                            ]
                        }
                    }
                },
                "122489030": {
                    "name": "Sonho dos Móveis",
                    "properties": {
                        "UA-122489030-1": {
                            "custom_metrics": [

                            ],
                            "profiles": [
                                {
                                    "id": "178643400",
                                    "name": "Todos os dados do website"
                                }
                            ]
                        }
                    }
                },
                "187669733": {
                    "name": "Melhor Código",
                    "properties": {

                    }
                },
                "188017198": {
                    "name": "Aporte Fácil",
                    "properties": {

                    }
                },
                "76876633": {
                    "name": "AdMob pub-2813072672105928",
                    "properties": {
                        "UA-76876633-1": {
                            "custom_metrics": [

                            ],
                            "profiles": [
                                {
                                    "id": "120931300",
                                    "name": "Default view"
                                }
                            ]
                        },
                        "UA-76876633-2": {
                            "custom_metrics": [

                            ],
                            "profiles": [
                                {
                                    "id": "120892861",
                                    "name": "Default view"
                                }
                            ]
                        },
                        "UA-76876633-3": {
                            "custom_metrics": [

                            ],
                            "profiles": [
                                {
                                    "id": "120892862",
                                    "name": "Default view"
                                }
                            ]
                        },
                        "UA-76876633-4": {
                            "custom_metrics": [

                            ],
                            "profiles": [
                                {
                                    "id": "120892863",
                                    "name": "Default view"
                                }
                            ]
                        },
                        "UA-76876633-5": {
                            "custom_metrics": [

                            ],
                            "profiles": [
                                {
                                    "id": "120892864",
                                    "name": "Default view"
                                }
                            ]
                        },
                        "UA-76876633-6": {
                            "custom_metrics": [

                            ],
                            "profiles": [
                                {
                                    "id": "173276223",
                                    "name": "All Web Site Data"
                                }
                            ]
                        }
                    }
                }
            },
            "ga_fields": {
                "dimensions": [
                    {
                        "id": "ga:campaign",
                        "name": "Campaign"
                    }
                ],
                "metrics": [
                    {
                        "id": "ga:transactionRevenue",
                        "name": "Revenue"
                    }
                ]
            }
        }


class GoogleConnector(BaseConnector):
    TYPE = 'google'

    def __init__(self, client_id, client_secret, developer_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.developer_token = developer_token

    @property
    def type(self):
        return GoogleConnector.TYPE

    def build_connector(self, connector_configuration):
        options = self.load_options(None)
        return Connector(self.type, None, options)

    def load_options(self, connector_configuration):
        return GOOGLE_MOCK_CONNECTOR_OPTIONS
