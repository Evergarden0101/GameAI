// DemoRecorderMenu.cs — a menu toggle to record human demonstrations
// ------------------------------------------------------------------
// Adds "RollerBall ▸ Record Demonstrations (WASD)" to the Unity menu bar. When it's
// checked, EnvironmentBuilder puts the agent in Heuristic mode and attaches a
// Demonstration Recorder on Play, so you can drive with WASD and capture a .demo file.
//
// Editor-only: this file lives in an Editor/ folder and is compiled only in the Editor.

#if UNITY_EDITOR
using UnityEditor;

public static class DemoRecorderMenu
{
    const string Key  = "RollerBall.RecordDemo";
    const string Path = "RollerBall/Record Demonstrations (WASD)";

    // Toggle the flag.
    [MenuItem(Path, priority = 0)]
    static void Toggle()
    {
        bool on = !EditorPrefs.GetBool(Key, false);
        EditorPrefs.SetBool(Key, on);
        if (on)
            EditorUtility.DisplayDialog("Record Demonstrations",
                "Recording is ON.\n\nPress Play and drive with WASD to capture a demo, " +
                "then STOP Play — it saves to Assets/Demonstrations/RollerBall.demo.\n\n" +
                "Turn this off before training normally.", "OK");
    }

    // Show a checkmark next to the menu item when recording is enabled.
    [MenuItem(Path, validate = true)]
    static bool ToggleValidate()
    {
        Menu.SetChecked(Path, EditorPrefs.GetBool(Key, false));
        return true;
    }
}
#endif
