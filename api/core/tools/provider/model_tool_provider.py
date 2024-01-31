from typing import List, Dict, Any
from pydantic import BaseModel
from os import path
from yaml import load, FullLoader

from core.tools.entities.tool_entities import ToolProviderType, \
      ToolParameter, ToolProviderCredentials, ToolDescription, ToolProviderIdentity
from core.tools.provider.tool_provider import ToolProviderController
from core.tools.errors import ToolNotFoundError
from core.tools.tool.model_tool import ModelTool
from core.tools.tool.tool import Tool
from core.tools.entities.tool_entities import ToolIdentity
from core.tools.entities.common_entities import I18nObject
from core.model_runtime.entities.model_entities import ModelType, ModelFeature
from core.entities.model_entities import ModelStatus
from core.provider_manager import ProviderManager, ProviderConfiguration, ProviderModelBundle
from core.model_manager import ModelInstance

class ModelToolProviderConfiguration(BaseModel):
    """
        the configuration of the model tool provider
    """
    class Provider(BaseModel):
        class Model(BaseModel):
            name: str
            alias: I18nObject = None

        provider: str
        alias: I18nObject = None
        models: List[Model] = None

    providers: List[Provider] = None

_model_tool_provider_config: ModelToolProviderConfiguration = None
with open(path.join(path.dirname(__file__), '_model_providers.yaml'), 'r') as f:
    _model_tool_provider_config = ModelToolProviderConfiguration(**load(f, Loader=FullLoader))

class ModelToolProviderController(ToolProviderController):
    configuration: ProviderConfiguration = None
    is_active: bool = False

    def __init__(self, configuration: ProviderConfiguration = None, **kwargs):
        """
            init the provider

            :param data: the data of the provider
        """
        super().__init__(**kwargs)
        self.configuration = configuration

    @staticmethod
    def from_db(configuration: ProviderConfiguration = None) -> 'ModelToolProviderController':
        """
            init the provider from db

            :param configuration: the configuration of the provider
        """
        # check if all models are active
        if configuration is None:
            return None
        is_active = True
        models = configuration.get_provider_models()
        for model in models:
            if model.status != ModelStatus.ACTIVE:
                is_active = False
                break

        # override the configuration
        for provider in _model_tool_provider_config.providers:
            if provider.provider == configuration.provider.provider:
                configuration.provider.label.en_US = provider.alias.en_US
                configuration.provider.label.zh_Hans = provider.alias.zh_Hans
                break

        return ModelToolProviderController(
            is_active=is_active,
            identity=ToolProviderIdentity(
                author='Dify',
                name=configuration.provider.provider,
                description=I18nObject(
                    zh_Hans=f'{configuration.provider.label.zh_Hans} 模型能力提供商', 
                    en_US=f'{configuration.provider.label.en_US} model capability provider'
                ),
                label=I18nObject(
                    zh_Hans=configuration.provider.label.zh_Hans,
                    en_US=configuration.provider.label.en_US
                ),
                icon=configuration.provider.icon_small.en_US,
            ),
            configuration=configuration,
            credentials_schema={},
        )
    
    @staticmethod
    def is_configuration_valid(configuration: ProviderConfiguration) -> bool:
        """
            check if the configuration has a model can be used as a tool
        """
        models = configuration.get_provider_models()
        for model in models:
            if model.model_type == ModelType.LLM and ModelFeature.VISION in (model.features or []):
                return True
        return False

    def _get_model_tools(self, tenant_id: str = None) -> List[ModelTool]:
        """
            returns a list of tools that the provider can provide

            :return: list of tools
        """
        tenant_id = tenant_id or 'ffffffff-ffff-ffff-ffff-ffffffffffff'
        provider_manager = ProviderManager()
        if self.configuration is None:
            configurations = provider_manager.get_configurations(tenant_id=tenant_id).values()
            self.configuration = next(filter(lambda x: x.provider == self.identity.name, configurations), None)
        # get all tools
        tools: List[ModelTool] = []
        # get all models
        if not self.configuration:
            return tools
        configuration = self.configuration

        provider_configuration = next(filter(
            lambda x: x.provider == self.configuration.provider.provider, _model_tool_provider_config.providers
        ), None)

        for model in configuration.get_provider_models():
            if model.model_type == ModelType.LLM and ModelFeature.VISION in (model.features or []):
                # override the configuration
                if provider_configuration is not None:
                    for model_config in provider_configuration.models or []:
                        if model_config.name == model.model:
                            model.label.en_US = model_config.alias.en_US
                            model.label.zh_Hans = model_config.alias.zh_Hans
                            break
                
                provider_instance = configuration.get_provider_instance()
                model_type_instance = provider_instance.get_model_instance(model.model_type)
                provider_model_bundle = ProviderModelBundle(
                    configuration=configuration,
                    provider_instance=provider_instance,
                    model_type_instance=model_type_instance
                )

                model_instance = ModelInstance(provider_model_bundle, model.model)
                
                tools.append(ModelTool(
                    identity=ToolIdentity(
                        author='Dify',
                        name=model.model,
                        label=I18nObject(zh_Hans=model.label.zh_Hans, en_US=model.label.en_US),
                    ),
                    parameters=[
                        ToolParameter(
                            name='image_id',
                            label=I18nObject(zh_Hans='图片ID', en_US='Image ID'),
                            human_description=I18nObject(zh_Hans='图片ID', en_US='Image ID'),
                            type=ToolParameter.ToolParameterType.STRING,
                            form=ToolParameter.ToolParameterForm.LLM,
                            required=True,
                            default=Tool.VARIABLE_KEY.IMAGE.value
                        )
                    ],
                    description=ToolDescription(
                        human=I18nObject(zh_Hans='图生文工具', en_US='Convert image to text'),
                        llm='Vision tool used to extract text and other visual information from images, can be used for OCR, image captioning, etc.',
                    ),
                    is_team_authorization=model.status == ModelStatus.ACTIVE,
                    tool_type=ModelTool.ModelToolType.VISION,
                    _model_instance=model_instance,
                    _model=model.model,
                ))

        self.tools = tools
        return tools
    
    def get_credentials_schema(self) -> Dict[str, ToolProviderCredentials]:
        """
            returns the credentials schema of the provider

            :return: the credentials schema
        """
        return {}

    def get_tools(self, user_id: str, tenant_id: str) -> List[ModelTool]:
        """
            returns a list of tools that the provider can provide

            :return: list of tools
        """
        return self._get_model_tools(tenant_id=tenant_id)
    
    def get_tool(self, tool_name: str) -> ModelTool:
        """
            get tool by name

            :param tool_name: the name of the tool
            :return: the tool
        """
        if self.tools is None:
            self.get_tools()

        for tool in self.tools:
            if tool.identity.name == tool_name:
                return tool

        raise ValueError(f'tool {tool_name} not found')

    def get_parameters(self, tool_name: str) -> List[ToolParameter]:
        """
            returns the parameters of the tool

            :param tool_name: the name of the tool, defined in `get_tools`
            :return: list of parameters
        """
        tool = next(filter(lambda x: x.identity.name == tool_name, self.get_tools()), None)
        if tool is None:
            raise ToolNotFoundError(f'tool {tool_name} not found')
        return tool.parameters

    @property
    def app_type(self) -> ToolProviderType:
        """
            returns the type of the provider

            :return: type of the provider
        """
        return ToolProviderType.MODEL
    
    def validate_credentials(self, credentials: Dict[str, Any]) -> None:
        """
            validate the credentials of the provider

            :param tool_name: the name of the tool, defined in `get_tools`
            :param credentials: the credentials of the tool
        """
        pass

    def _validate_credentials(self, credentials: Dict[str, Any]) -> None:
        """
            validate the credentials of the provider

            :param tool_name: the name of the tool, defined in `get_tools`
            :param credentials: the credentials of the tool
        """
        pass