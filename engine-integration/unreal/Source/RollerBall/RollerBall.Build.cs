using UnrealBuildTool;

public class RollerBall : ModuleRules
{
    public RollerBall(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core", "CoreUObject", "Engine", "InputCore",

            // Learning Agents (experimental). In some UE versions the training code
            // lives in a separate "LearningAgentsTraining" module — both are listed.
            "LearningAgents",
            "LearningAgentsTraining",

            // Neural Network Engine — for running trained ONNX models at runtime.
            "NNE"
        });
    }
}
