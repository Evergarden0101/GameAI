using UnrealBuildTool;

public class RollerBallEditorTarget : TargetRules
{
    public RollerBallEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_4;
        ExtraModuleNames.Add("RollerBall");
    }
}
