import SwiftUI
import ComposableArchitecture

// MARK: - Preview all feature Views in a VStack

public struct AllPreviews_Preview: PreviewProvider {

    public static var previews: some View {
        VStack {
            Spacer()
{% for feature in allFeatures %}
            {{ feature.viewName }}(store: StoreOf<{{ feature.featureName }}>(
                initialState: .init()) {
                    {{ feature.featureName }}()
                }
//                 withDependencies: {
//                     $0.someDependency = something
//                 }
            )
            Spacer()
{% endfor %}
       }
    }
}
