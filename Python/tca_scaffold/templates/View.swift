// MARK: - View

public struct {{ viewName }}: View {

    private let store: StoreOf<{{ featureName }}>

    public init(
        store: StoreOf<{{ featureName }}>
    ) {
        self.store = store
    }

    public var body: some View {
        WithViewStore(store) { viewStore in
            // content here
        }
    }
}

// MARK: - Preview

public struct {{ viewName }}_Preview: PreviewProvider {

    public static var previews: some View {
        {{ viewName }}(store: StoreOf<{{ featureName }}>(
                initialState: .init(),
                reducer: {{ featureNAme }}()
            ))
        }
    }
}
