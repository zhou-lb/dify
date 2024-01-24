所以你想要为 Dify 做贡献 - 这太棒了，我们迫不及待地想看到你的贡献。作为一家拥有有限人数和资金的初创公司，我们有着设计最直观的工作流程来构建和管理 LLM 应用程序的宏伟目标。来自社区的任何帮助都是重要的。

鉴于我们的现状，我们需要灵活和快速地交付，但我们也希望确保像你这样的贡献者在贡献过程中能够获得尽可能顺畅的体验。我们为此编写了这份贡献指南，旨在让你熟悉代码库和我们与贡献者的工作方式，以便你能够快速进入有趣的部分。

这份指南和 Dify 本身一样，是一个不断发展的工作。如果有时它落后于实际项目，我们非常感谢你的理解，并欢迎任何改进的反馈。

在许可方面，请花一分钟阅读我们简短的[许可证和贡献者协议](./license)。社区还遵守[行为准则](https://github.com/langgenius/.github/blob/main/CODE_OF_CONDUCT.md)。

## 在开始之前

[查找](https://github.com/langgenius/dify/issues?q=is:issue+is:closed)一个现有的问题，或者[创建](https://github.com/langgenius/dify/issues/new/choose)一个新问题。我们将问题分为两类：

### 功能请求：

* 如果你要提出一个新的功能请求，我们希望你解释一下所提议的功能的目标，并尽可能提供足够的上下文。[@perzeusss](https://github.com/perzeuss)制作了一个很好的[Feature Request Copilot](https://udify.app/chat/MK2kVSnw1gakVwMX)，可以帮助你起草你的需求。随时试试看。

* 如果你想从现有的问题中选择一个问题，只需在其下方留下一条评论即可。

  相关方向的团队成员将被卷入其中。如果一切看起来都很好，他们将批准你开始编码。在那之前，请不要开始处理该功能，以免你的工作在我们提出更改时被浪费。

  根据所提议的功能所属的领域的不同，你可能需要与不同的团队成员交流。以下是我们的团队成员目前正在从事的各个领域的概述：

  | Member                                                       | Scope                                                |
  | ------------------------------------------------------------ | ---------------------------------------------------- |
  | [@yeuoly](https://github.com/Yeuoly)                         | Architecting Agents                                  |
  | [@jyong](https://github.com/JohnJyong)                       | RAG pipeline design                                  |
  | [@GarfieldDai](https://github.com/GarfieldDai)               | Building workflow orchestrations                     |
  | [@iamjoel](https://github.com/iamjoel) & [@zxhlyh](https://github.com/zxhlyh) | Making our frontend a breeze to use                  |
  | [@guchenhe](https://github.com/guchenhe) & [@crazywoola](https://github.com/crazywoola) | Developer experience, points of contact for anything |
  | [@takatost](https://github.com/takatost)                     | Overall product direction and architecture           |

  我们的优先级：

  | 功能类型                                                     | 优先级          |
  | ------------------------------------------------------------ | --------------- |
  | 团队成员标记为高优先级的高优先级功能                         | 高优先级        |
  | 来自我们的[社区反馈板](https://feedback.dify.ai/)的热门功能请求 | 中优先级        |
  | 非核心功能和次要增强                                         | 低优先级        |
  | 有价值但不是立即实施的功能                                   | 未来功能        |

### 其他任何事项（例如错误报告、性能优化、拼写错误更正）：

* 立即开始编码。

  我们的优先级：

  | 问题类型                                                     | 优先级          |
  | ------------------------------------------------------------ | --------------- |
  | 核心功能中的错误（无法登录、应用程序无法工作、安全漏洞）       | 临界            |
  | 非临界错误、性能提升                                         | 中优先级        |
  | 小修复（拼写错误、界面令人困惑但可用的 UI）                   | 低优先级        |

### 4. Installations

Dify is composed of a backend and a frontend. Navigate to the backend directory by `cd api/`, then follow the [Backend README](api/README.md) to install it. In a separate terminal, navigate to the frontend directory by `cd web/`, then follow the [Frontend README](web/README.md) to install.

Check the [installation FAQ](https://docs.dify.ai/getting-started/faq/install-faq) for a list of common issues and steps to troubleshoot.

### 5. Visit dify in your browser

To validate your set up, head over to [http://localhost:3000](http://localhost:3000) (the default, or your self-configured URL and port) in your browser. You should now see Dify up and running. 

## Developing

If you are adding a model provider, [this guide](https://github.com/langgenius/dify/blob/main/api/core/model_runtime/README.md) is for you.

If you are adding a tool provider to Agent or Workflow, [this guide](./api/core/tools/README.md) is for you.

To help you quickly navigate where your contribution fits, a brief, annotated outline of Dify's backend & frontend is as follows:

### Backend

Dify’s backend is written in Python using [Flask](https://flask.palletsprojects.com/en/3.0.x/). It uses [SQLAlchemy](https://www.sqlalchemy.org/) for ORM and [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) for task queueing. Authorization logic goes via Flask-login. 

```
[api/]
├── constants             // Constant settings used throughout code base.
├── controllers           // API route definitions and request handling logic.           
├── core                  // Core application orchestration, model integrations, and tools.
├── docker                // Docker & containerization related configurations.
├── events                // Event handling and processing
├── extensions            // Extensions with 3rd party frameworks/platforms.
├── fields                // field definitions for serialization/marshalling.
├── libs                  // Reusable libraries and helpers.
├── migrations            // Scripts for database migration.
├── models                // Database models & schema definitions.
├── services              // Specifies business logic.
├── storage               // Private key storage.      
├── tasks                 // Handling of async tasks and background jobs.
└── tests
```

### Frontend

The website is bootstrapped on [Next.js](https://nextjs.org/) boilerplate in Typescript and uses [Tailwind CSS](https://tailwindcss.com/) for styling. [React-i18next](https://react.i18next.com/) is used for internationalization.

```
[web/]
├── app                   // layouts, pages, and components
│   ├── (commonLayout)    // common layout used throughout the app
│   ├── (shareLayout)     // layouts specifically shared across token-specific sessions 
│   ├── activate          // activate page
│   ├── components        // shared by pages and layouts
│   ├── install           // install page
│   ├── signin            // signin page
│   └── styles            // globally shared styles
├── assets                // Static assets
├── bin                   // scripts ran at build step
├── config                // adjustable settings and options 
├── context               // shared contexts used by different portions of the app
├── dictionaries          // Language-specific translate files 
├── docker                // container configurations
├── hooks                 // Reusable hooks
├── i18n                  // Internationalization configuration
├── models                // describes data models & shapes of API responses
├── public                // meta assets like favicon
├── service               // specifies shapes of API actions
├── test                  
├── types                 // descriptions of function params and return values
└── utils                 // Shared utility functions
```

## Submitting your PR

At last, time to open a pull request (PR) to our repo. For major features, we first merge them into the `deploy/dev` branch for testing, before they go into the `main` branch. If you run into issues like merge conflicts or don't know how to open a pull request, check out [GitHub's pull request tutorial](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests). 

And that's it! Once your PR is merged, you will be featured as a contributor in our [README](https://github.com/langgenius/dify/blob/main/README.md).

## Getting Help

If you ever get stuck or got a burning question while contributing, simply shoot your queries our way via the related GitHub issue, or hop onto our [Discord](https://discord.gg/AhzKf7dNgk) for a quick chat. 

