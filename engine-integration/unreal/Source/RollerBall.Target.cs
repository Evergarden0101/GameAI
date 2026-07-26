using UnrealBuildTool;

public class RollerBallTarget : TargetRules
{
    public RollerBallTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_4;
        ExtraModuleNames.Add("RollerBall");
    }
}
