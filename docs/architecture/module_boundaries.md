# Module Boundaries

依赖方向遵循 Clean Architecture。领域层不依赖基础设施；应用层编排领域端口；基础设施和集成层实现端口；工作流不读取其他工作流内部 State。

